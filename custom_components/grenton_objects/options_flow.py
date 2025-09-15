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
    DOMAIN,
    CONF_API_ENDPOINT
)

class GrentonOptionsFlowHandler(config_entries.OptionsFlow):

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        default_endpoint = self.config_entry.options.get(
            CONF_API_ENDPOINT,
            self.config_entry.data.get(CONF_API_ENDPOINT)
        )

        data_schema = vol.Schema({
            vol.Required(CONF_API_ENDPOINT, default=default_endpoint): str
        })
        return self.async_show_form(step_id="init", data_schema=data_schema)