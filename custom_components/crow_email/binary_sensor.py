"""Binary sensors for each email account: Connected, and New Mail."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import CrowEmailEntity, setup_platform
from .manager import Account


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, add: AddEntitiesCallback) -> None:
    setup_platform(hass, entry, add, lambda a: [ConnectedSensor(a), NewMailSensor(a)])


class ConnectedSensor(CrowEmailEntity, BinarySensorEntity):
    """On while Home Assistant is signed in to the mail server."""
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, a: Account) -> None:
        super().__init__(a, "connected")

    @property
    def is_on(self):
        return bool(self.stats.get("connected"))

    @property
    def extra_state_attributes(self):
        return {"error": self.stats.get("error") or None}


class NewMailSensor(CrowEmailEntity, BinarySensorEntity):
    """On when unread mail has arrived since the Inbox was last looked at in the card."""
    _attr_icon = "mdi:email-alert"

    def __init__(self, a: Account) -> None:
        super().__init__(a, "new_mail")

    @property
    def is_on(self):
        return bool(self.stats.get("new_mail"))
