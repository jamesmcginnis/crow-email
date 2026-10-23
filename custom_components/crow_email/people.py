"""Each person's contacts and card backgrounds, kept private to them.

Contacts follow the vCard fields, so they can be imported from and exported to phones. Backgrounds
are a photo (a data URL, resized in the card) or a Live Wallpaper ("live:<name>"), for every
mailbox ("*") or for one mailbox.
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONTACT_TEXT_FIELDS = (
    "prefix", "first", "middle", "last", "suffix", "nickname", "pronouns",
    "phonetic_first", "phonetic_last", "company", "job_title", "department",
    "notes", "birthday",
)
CONTACT_LIST_FIELDS = ("phones", "emails", "urls", "addresses", "dates", "related", "social")
ADDRESS_KEYS = ("label", "street", "city", "county", "postcode", "country")
MAX_CONTACTS = 5000
MAX_PHOTO = 400_000
MAX_BACKGROUND = 2_500_000
MAX_BACKGROUNDS = 40
LIVE_WALLPAPERS = ("rain", "aurora", "lava", "night", "fire", "ocean", "sky", "snowfall", "fireflies", "space", "fairy", "liquid")


class PeopleError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _clean(value: Any, limit: int = 2000) -> str:
    return "" if value is None else str(value).strip()[:limit]


def sanitize_contact(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise PeopleError("invalid", "A contact must be an object")
    out: dict[str, Any] = {}
    for key in CONTACT_TEXT_FIELDS:
        if raw.get(key):
            out[key] = _clean(raw[key], 10000 if key == "notes" else 300)
    photo = raw.get("photo")
    if photo:
        photo = str(photo)
        if not photo.startswith("data:image/") or len(photo) > MAX_PHOTO:
            raise PeopleError("invalid", "That contact photo is too large")
        out["photo"] = photo
    out["favourite"] = bool(raw.get("favourite"))
    for key in CONTACT_LIST_FIELDS:
        items = raw.get(key) or []
        if not isinstance(items, list):
            continue
        cleaned = []
        for item in items[:50]:
            if not isinstance(item, dict):
                continue
            if key == "addresses":
                entry = {k: _clean(item.get(k), 300) for k in ADDRESS_KEYS}
                if any(entry[k] for k in ADDRESS_KEYS if k != "label"):
                    cleaned.append(entry)
            else:
                entry = {"label": _clean(item.get("label"), 60), "value": _clean(item.get("value"), 500)}
                if key == "emails":
                    entry["value"] = entry["value"].lower()
                if entry["value"]:
                    cleaned.append(entry)
        if cleaned:
            out[key] = cleaned
    return out


class People:
    def __init__(self, hass: HomeAssistant, mailer) -> None:
        self.hass = hass
        self.mailer = mailer
        self.cstore = Store(hass, 1, f"{DOMAIN}.contacts", private=True, atomic_writes=True)
        self.bstore = Store(hass, 1, f"{DOMAIN}.backgrounds", private=True, atomic_writes=True)
        self.contacts: dict[str, dict[str, dict]] = {}
        self.backgrounds: dict[str, dict[str, str]] = {}
        self.stickers: dict = {"images": {}, "users": {}}

    async def async_load(self) -> None:
        self.contacts = (await self.cstore.async_load() or {}).get("contacts", {})
        bdata = await self.bstore.async_load() or {}
        self.backgrounds = bdata.get("users", {})
        self.stickers = bdata.get("stickers") or {"images": {}, "users": {}}

    def _save_contacts(self) -> None:
        self.cstore.async_delay_save(lambda: {"contacts": self.contacts}, 2)

    def _save_backgrounds(self) -> None:
        self.bstore.async_delay_save(lambda: {"users": self.backgrounds, "stickers": self.stickers}, 2)

    # ── stickers: each person's own ──
    def stickers_for(self, uid: str) -> list[str]:
        return list(self.stickers["users"].get(uid, []))

    def sticker_images(self, uid: str, ids: list[str]) -> dict:
        mine = set(self.stickers["users"].get(uid, []))
        return {i: self.stickers["images"][i] for i in ids[:200] if i in mine and i in self.stickers["images"]}

    def save_sticker(self, uid: str, image: str) -> str:
        import hashlib
        if not image.startswith(("data:image/png", "data:image/webp")) or len(image) > 600_000:
            raise PeopleError("invalid", "That sticker is too large.")
        mine = self.stickers["users"].setdefault(uid, [])
        sid = hashlib.sha256(image.encode()).hexdigest()[:32]
        if sid not in mine:
            if len(mine) >= 120:
                raise PeopleError("invalid", "You can keep up to 120 stickers.")
            self.stickers["images"][sid] = image
            mine.insert(0, sid)
            self._save_backgrounds()
        return sid

    def delete_sticker(self, uid: str, sid: str) -> None:
        mine = self.stickers["users"].get(uid, [])
        if sid in mine:
            mine.remove(sid)
            if not any(sid in v for v in self.stickers["users"].values()):
                self.stickers["images"].pop(sid, None)
            self._save_backgrounds()

    # ── contacts ─────────────────────────────────────────────────────────
    def contacts_for(self, uid: str) -> list[dict]:
        return list(self.contacts.get(uid, {}).values())

    def has_email(self, uid: str, email_addr: str) -> bool:
        e = (email_addr or "").lower()
        return any(x.get("value") == e for c in self.contacts.get(uid, {}).values() for x in c.get("emails") or [])

    def save_contacts(self, uid: str, contacts: list[dict]) -> list[dict]:
        from .manager import new_id, now_ms
        book = self.contacts.setdefault(uid, {})
        saved = []
        for raw in contacts:
            contact = sanitize_contact(raw)
            cid = str(raw.get("id") or "") or new_id()
            if cid not in book and len(book) >= MAX_CONTACTS:
                raise PeopleError("invalid", f"You can have up to {MAX_CONTACTS} contacts.")
            contact["id"] = cid
            contact["updated"] = now_ms()
            book[cid] = contact
            saved.append(contact)
        self._save_contacts()
        self.mailer.send_to(uid, {"type": "contacts", "contacts": self.contacts_for(uid)})
        return saved

    def delete_contacts(self, uid: str, ids: list[str]) -> None:
        book = self.contacts.get(uid, {})
        for cid in ids:
            book.pop(cid, None)
        self._save_contacts()
        self.mailer.send_to(uid, {"type": "contacts", "contacts": self.contacts_for(uid)})

    # ── backgrounds ──────────────────────────────────────────────────────
    def backgrounds_for(self, uid: str) -> dict:
        return dict(self.backgrounds.get(uid, {}))

    def set_background(self, uid: str, key: str, image: str | None) -> dict:
        key = _clean(key, 400) or "*"
        mine = self.backgrounds.setdefault(uid, {})
        if image:
            if image == "none":
                pass
            elif image.startswith("live:"):
                if image[5:] not in LIVE_WALLPAPERS:
                    raise PeopleError("invalid", "Unknown live wallpaper")
            elif not image.startswith("data:image/") or len(image) > MAX_BACKGROUND:
                raise PeopleError("invalid", "That picture is too large")
            if key not in mine and len(mine) >= MAX_BACKGROUNDS:
                raise PeopleError("invalid", "Too many backgrounds")
            mine[key] = image
        else:
            mine.pop(key, None)
        self._save_backgrounds()
        self.mailer.send_to(uid, {"type": "backgrounds", "backgrounds": self.backgrounds_for(uid)})
        return self.backgrounds_for(uid)
