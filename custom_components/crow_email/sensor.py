"""Sensors for each email account: unread, VIP, latest email, today, flagged, drafts, storage, last checked, parcels, junk."""
from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .entity import CrowEmailEntity, setup_platform
from .manager import Account


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, add: AddEntitiesCallback) -> None:
    def make(a: Account) -> list:
        return [UnreadSensor(a), UnreadVipSensor(a), LatestSensor(a), TodaySensor(a), FlaggedSensor(a),
                DraftsSensor(a), StorageSensor(a), LastCheckedSensor(a), ParcelsSensor(a), JunkSensor(a), BadgeSensor(a),
                AttentionTodaySensor(a), BillsDueSensor(a)]
    setup_platform(hass, entry, add, make)


class _Count(CrowEmailEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "emails"
    field = ""

    @property
    def native_value(self):
        return self.stats.get(self.field)


class UnreadSensor(_Count):
    _attr_icon = "mdi:email-mark-as-unread"
    field = "unread"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "unread")


class UnreadVipSensor(_Count):
    _attr_icon = "mdi:star-circle"
    field = "unread_vip"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "unread_vip")


class TodaySensor(_Count):
    _attr_icon = "mdi:email-receive"
    field = "received_today"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "received_today")


class FlaggedSensor(_Count):
    _attr_icon = "mdi:flag"
    field = "flagged"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "flagged")


class DraftsSensor(_Count):
    """Drafts waiting to be finished, plus emails waiting to Send Later."""
    _attr_icon = "mdi:email-edit"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "drafts_scheduled")

    @property
    def native_value(self):
        s = self.stats
        if s.get("drafts") is None:
            return None
        return int(s.get("drafts") or 0) + int(s.get("scheduled") or 0)

    @property
    def extra_state_attributes(self):
        s = self.stats
        rt = self.rt
        nxt = None
        if rt:
            times = sorted(x["at"] for x in rt.mailer.data["scheduled"] if x["account"] == rt.id and x.get("at") and not x.get("undo"))
            if times:
                nxt = dt_util.utc_from_timestamp(times[0] / 1000).isoformat()
        return {"drafts": s.get("drafts"), "scheduled": s.get("scheduled"), "next_scheduled": nxt}


class LatestSensor(CrowEmailEntity, SensorEntity):
    """The subject of the newest email in the Inbox, with who it's from."""
    _attr_icon = "mdi:email-newsletter"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "latest")

    @property
    def native_value(self):
        latest = self.stats.get("latest")
        if not latest:
            return None
        return (latest.get("subject") or "(No subject)")[:250]

    @property
    def extra_state_attributes(self):
        latest = self.stats.get("latest") or {}
        when = latest.get("date")
        return {
            "from_name": latest.get("from_name"),
            "from_email": latest.get("from_email"),
            "received": dt_util.utc_from_timestamp(when / 1000).isoformat() if when else None,
            "has_attachments": latest.get("attachments"),
            "vip": latest.get("vip"),
            "preview": latest.get("preview") or None,
        }


class StorageSensor(CrowEmailEntity, SensorEntity):
    _attr_icon = "mdi:harddisk"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, a: Account) -> None:
        super().__init__(a, "storage")

    @property
    def native_value(self):
        st = self.stats.get("storage")
        return st.get("percent") if st else None

    @property
    def extra_state_attributes(self):
        st = self.stats.get("storage") or {}
        mb = lambda v: round(v / 1048576, 1) if v else None  # noqa: E731
        return {"used_mb": mb(st.get("used")), "total_mb": mb(st.get("total"))}


class LastCheckedSensor(CrowEmailEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, a: Account) -> None:
        super().__init__(a, "last_checked")

    @property
    def native_value(self):
        v = self.stats.get("last_sync")
        return datetime.fromisoformat(v) if v else None


class ParcelsSensor(CrowEmailEntity, SensorEntity):
    """Parcel Tracker (an AI feature): deliveries on their way, found in email."""
    _attr_icon = "mdi:package-variant-closed"
    _attr_native_unit_of_measurement = "parcels"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "parcels")

    @property
    def available(self) -> bool:
        from . import ai
        return self.rt is not None and ai.on(self.hass, self.mailer, "parcels")

    @property
    def _list(self) -> list[dict]:
        return self.mailer.smart.parcels(self.account_id)

    @property
    def native_value(self):
        return sum(1 for p in self._list if p.get("status") != "delivered")

    @property
    def extra_state_attributes(self):
        today = dt_util.now().date().isoformat()
        rt = self.rt
        share = rt.acc.get("share_details", True) if rt else True
        waiting = [p for p in self._list if p.get("status") != "delivered"]
        return {
            "expected_today": sum(1 for p in waiting if p.get("expected") == today),
            "out_for_delivery": sum(1 for p in waiting if p.get("status") == "out_for_delivery"),
            "parcels": [{"item": p.get("item") if share else "", "retailer": p.get("retailer") if share else "",
                         "courier": p.get("courier"), "status": p.get("status"), "expected": p.get("expected") or None,
                         "tracking": p.get("tracking") if share else ""} for p in self._list],
        }


class JunkSensor(CrowEmailEntity, SensorEntity):
    """Email in the account's Junk (or Spam) folder."""
    _attr_icon = "mdi:email-alert"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "emails"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "junk")

    @property
    def native_value(self):
        j = self.stats.get("junk")
        return j.get("messages") if isinstance(j, dict) else None

    @property
    def extra_state_attributes(self):
        j = self.stats.get("junk")
        return {"unread": j.get("unseen") if isinstance(j, dict) else None}


class BadgeSensor(CrowEmailEntity, SensorEntity):
    """The number on the Home Assistant app's icon for the person who owns this account."""
    _attr_icon = "mdi:numeric-9-plus-circle"
    _attr_entity_registry_enabled_default = True

    def __init__(self, a: Account) -> None:
        super().__init__(a, "badge")

    @property
    def available(self) -> bool:
        return self.rt is not None and self.mailer.badge.enabled

    @property
    def native_value(self):
        rt = self.rt
        return self.mailer.badge.total(rt.acc["owner"]) if rt else None

    @property
    def extra_state_attributes(self):
        rt = self.rt
        if not rt:
            return {}
        uid = rt.acc["owner"]
        p = self.mailer.badge.prefs(uid)
        return {"counts": p["count"], "email": self.mailer.badge.email_count(uid),
                "extra": int(self.mailer.data["badge_extra"].get(uid) or 0)}


class AttentionTodaySensor(CrowEmailEntity, SensorEntity):
    """Today: parcels arriving, reminders due, snoozed emails coming back and follow-ups, for this account."""
    _attr_icon = "mdi:calendar-today"
    _attr_native_unit_of_measurement = "items"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "attention_today")

    @property
    def _items(self) -> list[dict]:
        rt = self.rt
        if not rt:
            return []
        try:
            return self.mailer.features.today_for(rt.acc["owner"], rt.id)
        except Exception:  # noqa: BLE001
            return []

    @property
    def native_value(self):
        return len(self._items) if self.rt else None

    @property
    def extra_state_attributes(self):
        rt = self.rt
        share = rt.acc.get("share_details", True) if rt else True
        items = self._items
        def pick(kind):
            return [{"title": x.get("title") if share else "", "detail": x.get("sub"), "at": x.get("at")} for x in items if x["kind"] == kind]
        return {"parcels": pick("parcel"), "reminders": pick("reminder"), "snoozed": pick("snoozed"), "follow_ups": pick("followup"),
                "appointments": pick("appointment"), "bills": pick("bill")}


class BillsDueSensor(CrowEmailEntity, SensorEntity):
    """Bills (found by the AI) due in the next 7 days, or overdue, and not marked paid."""
    _attr_icon = "mdi:cash-clock"
    _attr_native_unit_of_measurement = "bills"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "bills_due")

    @property
    def available(self) -> bool:
        from . import ai
        return self.rt is not None and ai.on(self.hass, self.mailer, "bills")

    @property
    def native_value(self):
        return len(self.mailer.aix.bills_due(self.account_id)) if self.rt else None

    @property
    def extra_state_attributes(self):
        rt = self.rt
        share = rt.acc.get("share_details", True) if rt else True
        due = self.mailer.aix.bills_due(self.account_id) if rt else []
        totals: dict[str, float] = {}
        for x in due:
            if x.get("amount") is not None:
                totals[x.get("currency") or ""] = round(totals.get(x.get("currency") or "", 0) + x["amount"], 2)
        return {"total": totals, "bills": [{"payee": x.get("payee") if share else "", "amount": x.get("amount"),
                                            "currency": x.get("currency"), "due": x.get("due"),
                                            "higher_than_last_time": x.get("higher")} for x in due]}
