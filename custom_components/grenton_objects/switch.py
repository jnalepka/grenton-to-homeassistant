"""
==================================================
Author: Jan Nalepka
Version: 2.1.1
Date: 2024-12-01
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import aiohttp
from .const import (
    DOMAIN,
    CONF_API_ENDPOINT,
    CONF_GRENTON_ID,
    CONF_OBJECT_NAME
)

import logging
import json
import voluptuous as vol
from homeassistant.components.switch import (
    SwitchEntity,
    PLATFORM_SCHEMA
)
from homeassistant.const import (STATE_ON, STATE_OFF)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Switch'): str
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    device = config_entry.data
    
    api_endpoint = device.get(CONF_API_ENDPOINT)
    grenton_id = device.get(CONF_GRENTON_ID)
    object_name = device.get(CONF_OBJECT_NAME)

    async_add_entities([GrentonSwitch(api_endpoint, grenton_id, object_name)], True)

class GrentonSwitch(SwitchEntity):
    def __init__(self, api_endpoint, grenton_id, object_name):
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._object_name = object_name
        self._state = None
        self._unique_id = f"grenton_{grenton_id.split('->')[1]}"

    @property
    def name(self):
        return self._object_name

    @property
    def is_on(self):
        return self._state == STATE_ON

    @property
    def unique_id(self):
        return self._unique_id

    async def async_turn_on(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:set(0, 1)')"}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    self._state = STATE_ON
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to turn on the switch: {ex}")

    async def async_turn_off(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:set(0, 0)')"}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    self._state = STATE_OFF
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to turn off the switch: {ex}")

    async def async_update(self):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"status": f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:get(0)')"}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self._state = STATE_OFF if data.get("status") == 0 else STATE_ON
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to update the switch state: {ex}")
            self._state = None
