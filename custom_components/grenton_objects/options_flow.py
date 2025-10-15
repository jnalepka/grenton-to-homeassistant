"""
==================================================
Author: Jan Nalepka
Script version: 3.1
Date: 16.10.2025
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import voluptuous as vol
from homeassistant import config_entries
from .const import (
    CONF_API_ENDPOINT,
    CONF_AUTO_UPDATE,
    CONF_UPDATE_INTERVAL, 
    DEFAULT_UPDATE_INTERVAL,
    CONF_REVERSED
)

class GrentonOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry
        self.device_type = config_entry.data.get("device_type", "")

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

        if self.device_type == "cover":
            default_reversed = self.config_entry.options.get(CONF_REVERSED, False)
            data_schema = data_schema.extend({
                vol.Required(CONF_REVERSED, default=default_reversed): bool
            })

        return self.async_show_form(step_id="init", data_schema=data_schema)