"""The red number on the Home Assistant app's icon: how much unread email you have.

iPhone and iPad: each Crow Email notification carries the number, and when it changes without
a notification (you read email somewhere else) a silent update ("delete_alert") sets it.
Whether or not the badge is on, notifications for email you've read are taken away on every phone
and tablet (on Android that's also what makes the app's dot go away).
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.core import callback
from homeassistant.helpers.event import async_call_later

if TYPE_CHECKING:
    from .manager import Account, Mailer

_LOGGER = logging.getLogger(__name__)

COUNTS = ("unread", "notified", "vip")
DEBOUNCE = 3


class Badge:
    def __init__(self, mailer: "Mailer") -> None:
        self.mailer = mailer
        self.hass = mailer.hass
        mailer.data.setdefault("badge_sent", {})
        mailer.data.setdefault("badge_extra", {})
        mailer.data.setdefault("notified", {})
        self._timers: dict[str, Any] = {}

    def unload(self) -> None:
        for cancel in self._timers.values():
            cancel()
        self._timers.clear()

    # ── settings ───────────────────────────────────────────────────────────
    @property
    def enabled(self) -> bool:
        return bool((self.mailer.settings.get("badge") or {}).get("enabled"))

    def prefs(self, uid: str) -> dict:
        p = (self.mailer.data["prefs"].get(uid) or {}).get("badge") or {}
        return {"on": p.get("on", True), "count": p.get("count") if p.get("count") in COUNTS else "unread"}

    def save_prefs(self, uid: str, d: dict) -> dict:
        cur = self.prefs(uid)
        if isinstance(d.get("on"), bool):
            cur["on"] = d["on"]
        if d.get("count") in COUNTS:
            cur["count"] = d["count"]
        self.mailer.data["prefs"].setdefault(uid, {})["badge"] = cur
        self.mailer.save()
        self.changed(uid, now=True)
        return cur

    # ── the number ─────────────────────────────────────────────────────────
    def email_count(self, uid: str) -> int:
        field = {"unread": "unread", "notified": "unread_notified", "vip": "unread_vip"}[self.prefs(uid)["count"]]
        return sum(int(a.stats.get(field) or 0) for a in self.mailer.accounts.values() if a.acc["owner"] == uid)

    def total(self, uid: str) -> int | None:
        """The badge for this person, or None if badges are off for them."""
        if not self.enabled or not uid:
            return None
        p = self.prefs(uid)
        if not p["on"]:
            return None
        return max(0, self.email_count(uid) + int(self.mailer.data["badge_extra"].get(uid) or 0))

    def state_for(self, uid: str) -> dict:
        return {"enabled": self.enabled, **self.prefs(uid), "total": self.total(uid)}

    @callback
    def sent(self, uid: str, n: int) -> None:
        """A notification just carried this number."""
        self.mailer.data["badge_sent"][uid] = n

    def for_notification(self, uid: str, extra: int = 0) -> int | None:
        n = self.total(uid)
        if n is None:
            return None
        n += extra
        self.sent(uid, n)
        return n

    def set_extra(self, uid: str, n: int) -> None:
        self.mailer.data["badge_extra"][uid] = max(0, int(n))
        self.mailer.save()
        self.changed(uid, now=True)

    # ── a silent update when the number changes without a notification ───────
    @callback
    def changed(self, uid: str, now: bool = False) -> None:
        if not self.enabled:
            return
        if uid in self._timers:
            self._timers.pop(uid)()

        async def go(_now=None) -> None:
            self._timers.pop(uid, None)
            await self.async_push(uid)
        if now:
            self.hass.async_create_task(go())
        else:
            self._timers[uid] = async_call_later(self.hass, DEBOUNCE, go)

    async def async_push(self, uid: str, force: bool = False) -> None:
        n = self.total(uid)
        if n is None:
            return
        if not force and self.mailer.data["badge_sent"].get(uid) == n:
            return
        self.sent(uid, n)
        self.mailer.save()
        for service, ios in self.devices(uid):
            if not ios:
                continue
            try:
                await self.hass.services.async_call("notify", service, {"message": "delete_alert", "data": {"push": {"badge": n}}})
            except Exception as err:  # noqa: BLE001
                _LOGGER.debug("Crow Email couldn't update the badge on %s: %s", service, err)
        for a in self.mailer.accounts.values():
            if a.acc["owner"] == uid:
                a.publish()
        self.mailer.send_to(uid, {"type": "badge", "badge": self.state_for(uid)})

    def devices(self, uid: str) -> list[tuple[str, bool]]:
        """This person's phones and tablets: (notify service, whether it's an iPhone or iPad)."""
        from homeassistant.util import slugify
        out = []
        for entry in self.hass.config_entries.async_entries("mobile_app"):
            if entry.data.get("user_id") != uid:
                continue
            service = f"mobile_app_{slugify(entry.data.get('device_name') or entry.title or '')}"
            if self.hass.services.has_service("notify", service):
                os_name = str(entry.data.get("os_name") or "").lower()
                out.append((service, os_name in ("ios", "ipados", "macos") or "iphone" in service or "ipad" in service))
        return out

    # ── notifications for email that's been read ────────────────────────────
    def note_notified(self, a: "Account", uid_: int) -> None:
        lst = self.mailer.data["notified"].setdefault(a.id, [])
        if uid_ not in lst:
            lst.append(uid_)
            del lst[:-400]
            self.mailer.save()

    def notified(self, account_id: str) -> list[int]:
        return self.mailer.data["notified"].get(account_id, [])

    async def async_clear(self, a: "Account", uids: list[int]) -> None:
        """Take away the notifications for email that's now been read - here or in another mail app -
        on every phone and tablet (on Android that's also what makes the app's dot go away)."""
        mine = set(self.notified(a.id))
        gone = [u for u in uids if u in mine]
        if not gone:
            return
        self.mailer.data["notified"][a.id] = [u for u in self.notified(a.id) if u not in gone]
        services = [s for s, _ios in self.devices(a.acc["owner"])]
        for u in gone[:20]:
            for service in services:
                try:
                    await self.hass.services.async_call("notify", service, {"message": "clear_notification",
                                                                            "data": {"tag": f"crow_email_{a.id}_{u}"}})
                except Exception:  # noqa: BLE001
                    pass
