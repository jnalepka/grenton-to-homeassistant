"""
==================================================
Author: Jan Nalepka
Script version: 3.1
Date: 01.10.2025
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import aiohttp
from .const import (
    CONF_API_ENDPOINT,
    CONF_GRENTON_ID,
    CONF_OBJECT_NAME,
    CONF_AUTO_UPDATE,
    CONF_UPDATE_INTERVAL, 
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN
)
import logging
import voluptuous as vol
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    PLATFORM_SCHEMA
)
from homeassistant.const import (STATE_ON, STATE_OFF)
from datetime import timedelta
from homeassistant.helpers.event import async_track_time_interval
import asyncio
import random

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Binary Sensor'): str
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_endpoint = config_entry.options.get(CONF_API_ENDPOINT, config_entry.data.get(CONF_API_ENDPOINT))
    grenton_id = config_entry.data.get(CONF_GRENTON_ID)
    object_name = config_entry.data.get(CONF_OBJECT_NAME)
    auto_update = config_entry.options.get(CONF_AUTO_UPDATE, True)
    update_interval = config_entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)

    entity = GrentonBinarySensor(api_endpoint, grenton_id, object_name, auto_update, update_interval)
    async_add_entities([entity], True)
    
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {"entities": {}}

    hass.data[DOMAIN]["entities"][entity.entity_id] = entity

class GrentonBinarySensor(BinarySensorEntity):
    def __init__(self, api_endpoint, grenton_id, object_name, auto_update, update_interval):
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._object_name = object_name
        self._unique_id = f"grenton_{grenton_id.split('->')[1]}"
        self._state = None
        self._auto_update = auto_update
        self._update_interval = update_interval
        self._unsub_interval = None
        self._initialized = False

    async def async_added_to_hass(self):
        await asyncio.sleep(random.uniform(0, self._update_interval))  # rozproszenie startu
        self._initialized = True
        if self._auto_update:
            self._unsub_interval = async_track_time_interval(
                self.hass, self._update_callback, timedelta(seconds=self._update_interval)
            )
            await self.async_update()

    async def async_will_remove_from_hass(self):
        if self._unsub_interval:
            self._unsub_interval()

    async def _update_callback(self, now):
        await self.async_update()

    async def async_force_state(self, state: int):
        self._state = STATE_ON if state == 1 else STATE_OFF
        self.async_write_ha_state()

    @property
    def name(self):
        return self._object_name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def is_on(self):
        return self._state == STATE_ON

    @property
    def should_poll(self):
        return False

    async def async_update(self):
        if not self._initialized:
            return

        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"status": f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:get(0)')"}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self._state = STATE_OFF if data.get("status") == 0 else STATE_ON
                    self.async_write_ha_state()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to update the binary sensor state: {ex}")
            self._state = None