"""
==================================================
Author: Jan Nalepka
Script version: 3.0
Date: 15.09.2025
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import aiohttp
import logging
import voluptuous as vol
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import Entity
from .const import (
    CONF_API_ENDPOINT,
    CONF_GRENTON_ID,
    CONF_OBJECT_NAME
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Script'): str
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_endpoint = config_entry.options.get(CONF_API_ENDPOINT, config_entry.data.get(CONF_API_ENDPOINT))
    grenton_id = config_entry.data.get(CONF_GRENTON_ID)
    object_name = config_entry.data.get(CONF_OBJECT_NAME)
    
    async_add_entities([GrentonScript(api_endpoint, grenton_id, object_name)], True)
    
    
class GrentonScript(ButtonEntity):
    def __init__(self, api_endpoint, grenton_id, object_name):
        self._object_name = object_name
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._unique_id = f"grenton_{grenton_id.split('->')[1] if '->' in grenton_id else grenton_id}"
        

    @property
    def name(self):
        return self._object_name
    
    @property
    def unique_id(self):
        return self._unique_id
    
    async def async_press(self):
        try:
            if '->' in self._grenton_id:
                grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
                command = {
                    "command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}(nil)')"
                }
            else:
                command = {
                    "command": f"{self._grenton_id}(nil)"
                }
            async with aiohttp.ClientSession() as session:
                async with session.post(self._api_endpoint, json=command) as response:
                    response.raise_for_status()
                    _LOGGER.info(f"Script {self._object_name} executed successfully (Grenton).")
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to execute script {self._object_name}: {ex}")
