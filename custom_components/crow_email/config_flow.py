"""Config flow for Crow Email."""
from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN


class CrowEmailConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """One step: each person adds their own email accounts in the card."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            return self.async_create_entry(title="Crow Email", data={})
        return self.async_show_form(step_id="user")
