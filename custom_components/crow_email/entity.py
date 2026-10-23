"""What every Crow Email entity shares: one device per email account, kept up to date live."""
from __future__ import annotations

from collections.abc import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, SIGNAL_ACCOUNT_UPDATED, SIGNAL_ACCOUNTS_CHANGED
from .manager import Account, Mailer


class CrowEmailEntity(Entity):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, account: Account, key: str) -> None:
        self.account_id = account.id
        self.mailer = account.mailer
        self.key = key
        self._attr_unique_id = f"{account.id}_{key}"
        self._attr_translation_key = key
        acc = account.acc
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, account.id)},
            name=f"{acc.get('name') or 'Email'} ({acc['email']})",
            manufacturer="Crow Email",
            model=acc.get("name") or acc.get("provider", "Email"),
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def rt(self) -> Account | None:
        return self.mailer.accounts.get(self.account_id)

    @property
    def stats(self) -> dict:
        rt = self.rt
        return rt.public_stats() if rt else {}

    @property
    def available(self) -> bool:
        return self.rt is not None

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(async_dispatcher_connect(
            self.hass, f"{SIGNAL_ACCOUNT_UPDATED}_{self.account_id}", self.async_write_ha_state))


def setup_platform(hass: HomeAssistant, entry: ConfigEntry, add: Callable, make: Callable[[Account], list]) -> None:
    """Entities for every account now, for accounts added later, and gone with deleted ones."""
    mailer: Mailer = hass.data[DOMAIN]
    known: set[str] = set()

    @callback
    def sync(removed: str | None = None) -> None:
        new = []
        for a in list(mailer.accounts.values()):
            if a.id not in known:
                known.add(a.id)
                new += make(a)
        if new:
            add(new)
        if removed:
            known.discard(removed)
            reg = er.async_get(hass)
            for ent in er.async_entries_for_config_entry(reg, entry.entry_id):
                if ent.unique_id.startswith(f"{removed}_"):
                    reg.async_remove(ent.entity_id)
            from homeassistant.helpers import device_registry as dr
            dreg = dr.async_get(hass)
            dev = dreg.async_get_device(identifiers={(DOMAIN, removed)})
            if dev:
                dreg.async_remove_device(dev.id)

    sync()
    entry.async_on_unload(async_dispatcher_connect(hass, SIGNAL_ACCOUNTS_CHANGED, sync))
