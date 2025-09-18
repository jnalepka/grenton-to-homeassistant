"""
==================================================
Author: Jan Nalepka
Script version: 3.0
Date: 15.09.2025
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import voluptuous as vol
from homeassistant import config_entries
from .const import (
    CONF_API_ENDPOINT,
    CONF_AUTO_UPDATE,
    CONF_UPDATE_INTERVAL, 
    DEFAULT_UPDATE_INTERVAL
)

class GrentonOptionsFlowHandler(config_entries.OptionsFlow):

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        default_endpoint = self.config_entry.options.get(
            CONF_API_ENDPOINT,
            self.config_entry.data.get(CONF_API_ENDPOINT)
        )

        default_auto_update = self.config_entry.options.get(CONF_AUTO_UPDATE, True)

        default_update_interval = self.config_entry.options.get(
            CONF_UPDATE_INTERVAL,
            DEFAULT_UPDATE_INTERVAL
        )

        data_schema = vol.Schema({
            vol.Required(CONF_API_ENDPOINT, default=default_endpoint): str,
            vol.Required(CONF_AUTO_UPDATE, default=default_auto_update): bool,
            vol.Required(CONF_UPDATE_INTERVAL, default=default_update_interval): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600))
        })
        return self.async_show_form(step_id="init", data_schema=data_schema)