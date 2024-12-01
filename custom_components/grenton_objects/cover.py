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
    CONF_OBJECT_NAME,
    CONF_REVERSED
)
import logging
import json
import voluptuous as vol
from homeassistant.components.cover import (
    CoverEntity,
    PLATFORM_SCHEMA,
    CoverDeviceClass
)
from homeassistant.const import (
    STATE_CLOSED,
    STATE_CLOSING,
    STATE_OPEN,
    STATE_OPENING
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Required(CONF_REVERSED, default=False): bool,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Cover'): str
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    device = config_entry.data
    
    api_endpoint = device.get(CONF_API_ENDPOINT)
    grenton_id = device.get(CONF_GRENTON_ID)
    reversed = device.get(CONF_REVERSED)
    object_name = device.get(CONF_OBJECT_NAME)

    async_add_entities([GrentonCover(api_endpoint, grenton_id, reversed, object_name)], True)

class GrentonCover(CoverEntity):
    def __init__(self, api_endpoint, grenton_id, reversed, object_name):
        self._device_class = CoverDeviceClass.BLIND
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._reversed = reversed
        self._object_name = object_name
        self._state = None
        self._current_cover_position = None
        self._current_cover_tilt_position = None
        self._unique_id = f"grenton_{grenton_id.split('->')[1]}"

    @property
    def name(self):
        return self._object_name

    @property
    def is_closed(self):
        return self._state == STATE_CLOSED

    @property
    def is_opening(self):
        return self._state == STATE_OPENING

    @property
    def is_closing(self):
        return self._state == STATE_CLOSING

    @property
    def current_cover_position(self):
        return self._current_cover_position
    
    @property
    def current_cover_tilt_position(self):
        return self._current_cover_tilt_position

    @property
    def unique_id(self):
        return self._unique_id

    async def async_open_cover(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(0, 0)')"}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    self._state = STATE_OPENING
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to open the cover: {ex}")

    async def async_close_cover(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(1, 0)')"}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    self._state = STATE_CLOSING
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to close the cover: {ex}")

    async def async_stop_cover(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(3, 0)')"}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    self._state = STATE_OPEN
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to stop the cover: {ex}")

    async def async_set_cover_position(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            position = kwargs.get("position", 100)
            self._current_cover_position = position
            if self._reversed == True:
                position = 100 - position
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(10, {position})')"}
            if grenton_id_part_1.startswith("ZWA"):
                command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(7, {position})')"}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    if (position > self._current_cover_position):
                        if self._reversed == True:
                            self._state = STATE_CLOSING
                        else:
                            self._state = STATE_OPENING
                    else:
                        if self._reversed == True:
                            self._state = STATE_OPENING
                        else:
                            self._state = STATE_CLOSING
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to set the cover position: {ex}")

    async def async_set_cover_tilt_position(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            tilt_position = kwargs.get("tilt_position", 90)
            self._current_cover_tilt_position = tilt_position
            tilt_position = tilt_position * 90 / 100
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(9, {tilt_position})')"}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to set the cover tilt position: {ex}")

    async def async_open_cover_tilt(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(9, 90)')"}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to open the cover tilt: {ex}")

    async def async_close_cover_tilt(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(9, 0)')"}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to close the cover tilt: {ex}")

    async def async_update(self):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            if grenton_id_part_1.startswith("ZWA"):
                command = {"status": f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:get(2)')"}
            else:
                command = {"status": f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:get(0)')"}
            if grenton_id_part_1.startswith("ZWA"):
                command.update({"status_2": f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:get(4)')"})
            else:
                command.update({"status_2": f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:get(7)')"})
            if grenton_id_part_1.startswith("ZWA"):
                command.update({"status_3": f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:get(6)')"})
            else:
                command.update({"status_3": f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:get(8)')"})
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self._state = STATE_CLOSED if data.get("status_2") == 0 else STATE_OPEN
                    if data.get("status") == 1:
                        if self._reversed == True:
                            self._state = STATE_CLOSING
                        else:
                            self._state = STATE_OPENING
                    elif data.get("status") == 2:
                        if self._reversed == True:
                            self._state = STATE_OPENING
                        else:
                            self._state = STATE_CLOSING
                    temp_position = data.get("status_2")
                    if self._reversed == True:
                        temp_position = 100 - temp_position
                    self._current_cover_position = temp_position
                    self._current_cover_tilt_position = data.get("status_3") * 100 / 90
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to update the cover state: {ex}")
            self._state = None
