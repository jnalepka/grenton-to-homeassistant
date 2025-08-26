"""
==================================================
Author: Jan Nalepka
Script version: 2.0
Date: 02.12.2024
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import aiohttp
from .const import (
    DOMAIN,
    CONF_API_ENDPOINT,
    CONF_GRENTON_ID,
    CONF_OBJECT_NAME,
    CONF_POLLING
)
import logging
import json
import voluptuous as vol
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    PLATFORM_SCHEMA
)
from homeassistant.const import (STATE_ON, STATE_OFF)
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Binary Sensor'): str,
    vol.Optional(CONF_POLLING, default=True): cv.boolean,
})

PUSH_UPDATE_SERVICE_SCHEMA = vol.Schema({
    vol.Required("entity_id"): cv.entity_id,
    vol.Required("value"): vol.Any(int, bool, str),
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    device = config_entry.data
    
    api_endpoint = device.get(CONF_API_ENDPOINT)
    grenton_id = device.get(CONF_GRENTON_ID)
    object_name = device.get(CONF_OBJECT_NAME)
    polling = device.get(CONF_POLLING, True)

    async_add_entities([GrentonBinarySensor(api_endpoint, grenton_id, object_name, polling)], True)
    
    async def handle_push_update(call):
        entity_id = call.data.get("entity_id")
        value = call.data.get("value")
        if entity_id == sensor.entity_id:
            await sensor.async_push_update(value)
            
    hass.services.async_register(
        DOMAIN,
        "push_update",
        handle_push_update,
        schema=PUSH_UPDATE_SERVICE_SCHEMA,
    )

class GrentonBinarySensor(BinarySensorEntity):
    def __init__(self, api_endpoint, grenton_id, object_name, polling):
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._object_name = object_name
        self._polling = polling
        self._unique_id = f"grenton_{grenton_id.split('->')[1]}"
        self._state = None

    @property
    def name(self):
        return self._object_name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def is_on(self):
        return self._state == STATE_ON

    async def async_update(self):
        if not self._polling:
            return
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"status": f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:get(0)')"}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self._state = STATE_OFF if data.get("status") == 0 else STATE_ON
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to update the binary sensor state: {ex}")
            self._state = None
            
    async def async_push_update(self, value):
        _LOGGER.debug(f"Received push update for {self.entity_id} with value: {value}")
        self._state = STATE_ON if value in (1, True, "1", "on") else STATE_OFF
        self.async_write_ha_state()  # Update Home Assistant state