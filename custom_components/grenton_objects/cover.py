"""
==================================================
Author: Jan Nalepka
Script version: 3.4
Date: 29.10.2025
Repository: https://github.com/jnalepka/grenton-objects-home-assistant
==================================================
"""

import aiohttp
from .const import (
    CONF_API_ENDPOINT,
    CONF_GRENTON_ID,
    CONF_OBJECT_NAME,
    CONF_REVERSED,
    CONF_REVERSED_TILT,
    CONF_AUTO_UPDATE,
    CONF_UPDATE_INTERVAL, 
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    CONF_DEVICE_CLASS
)
import logging
import voluptuous as vol
from homeassistant.components.cover import (
    CoverEntity,
    PLATFORM_SCHEMA,
    CoverDeviceClass,
    CoverEntityFeature
)
from homeassistant.const import (
    STATE_CLOSED,
    STATE_CLOSING,
    STATE_OPEN,
    STATE_OPENING
)
from datetime import timedelta
from homeassistant.helpers.event import async_track_time_interval

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Required(CONF_REVERSED, default=False): bool,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Cover'): str,
    vol.Optional(CONF_DEVICE_CLASS, default=''): str,
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_endpoint = config_entry.options.get(CONF_API_ENDPOINT, config_entry.data.get(CONF_API_ENDPOINT))
    grenton_id = config_entry.data.get(CONF_GRENTON_ID)
    reversed = config_entry.options.get(CONF_REVERSED, config_entry.data.get(CONF_REVERSED))
    reversed_tilt = config_entry.options.get(CONF_REVERSED_TILT, config_entry.data.get(CONF_REVERSED_TILT, False))
    object_name = config_entry.data.get(CONF_OBJECT_NAME)
    auto_update = config_entry.options.get(CONF_AUTO_UPDATE, config_entry.data.get(CONF_AUTO_UPDATE, True))
    update_interval = config_entry.options.get(CONF_UPDATE_INTERVAL, config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL))
    device_class = config_entry.options.get(CONF_DEVICE_CLASS, config_entry.data.get(CONF_DEVICE_CLASS, CoverDeviceClass.BLIND.value))

    entity = GrentonCover(api_endpoint, grenton_id, reversed, reversed_tilt, object_name, auto_update, update_interval, device_class)
    async_add_entities([entity], True)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {"entities": {}}

    hass.data[DOMAIN]["entities"][entity.entity_id] = entity

class GrentonCover(CoverEntity):
    def __init__(self, api_endpoint, grenton_id, reversed, reversed_tilt, object_name, auto_update, update_interval, device_class):
        self._device_class = device_class
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._reversed = reversed
        self._reversed_tilt = reversed_tilt
        self._object_name = object_name
        self._state = None
        self._current_cover_position = 0
        self._current_cover_tilt_position = 0
        self._unique_id = f"grenton_{grenton_id.split('->')[1]}"
        self._last_command_time = None
        self._auto_update = auto_update
        self._update_interval = update_interval
        self._unsub_interval = None
        self._initialized = False

    async def async_added_to_hass(self):
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

    async def async_force_cover(self, state: int, position: int, lamel: int):
        if self._reversed:
            position = 100 - position
        self._state = STATE_CLOSED if position == 0 else STATE_OPEN
        if state == 1:
            self._state = STATE_OPENING
        elif state == 2:
            self._state = STATE_CLOSING
        self._current_cover_position = position
        if lamel is not None:
            tilt_position = int(lamel * 100 / 90)
            if self._reversed_tilt:
                tilt_position = 100 - tilt_position
            self._current_cover_tilt_position = tilt_position
        self.async_write_ha_state()

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
    
    @property
    def should_poll(self):
        return False
    
    @property
    def device_class(self):
        return self._device_class
    
    @property
    def supported_features(self):
        base_features = (
            CoverEntityFeature.OPEN
            | CoverEntityFeature.CLOSE
            | CoverEntityFeature.STOP
            | CoverEntityFeature.SET_POSITION
        )

        if self._device_class == CoverDeviceClass.BLIND.value:
            base_features |= (
                CoverEntityFeature.OPEN_TILT
                | CoverEntityFeature.CLOSE_TILT
                | CoverEntityFeature.STOP_TILT
                | CoverEntityFeature.SET_TILT_POSITION
            )

        return base_features

    async def async_open_cover(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(0, 0)')"}
            self._state = STATE_OPENING
            self._last_command_time = self.hass.loop.time() if self.hass is not None else None
            self.async_write_ha_state()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to open the cover: {ex}")

    async def async_close_cover(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(1, 0)')"}
            self._state = STATE_CLOSING
            self._last_command_time = self.hass.loop.time() if self.hass is not None else None
            self.async_write_ha_state()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to close the cover: {ex}")

    async def async_stop_cover(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(3, 0)')"}
            self._state = STATE_OPEN
            self._last_command_time = self.hass.loop.time() if self.hass is not None else None
            self.async_write_ha_state()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to stop the cover: {ex}")

    async def async_set_cover_position(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            position = kwargs.get("position", 100)
            prev_position = self._current_cover_position
            self._current_cover_position = position
            if self._reversed:
                position = 100 - position
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(10, {position})')"}
            if grenton_id_part_1.startswith("ZWA"):
                command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(7, {position})')"}
            if (position > prev_position):
                if self._reversed:
                    self._state = STATE_CLOSING
                else:
                    self._state = STATE_OPENING
            else:
                if self._reversed:
                    self._state = STATE_OPENING
                else:
                    self._state = STATE_CLOSING
            self._last_command_time = self.hass.loop.time() if self.hass is not None else None
            self.async_write_ha_state()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to set the cover position: {ex}")

    async def async_set_cover_tilt_position(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            tilt_position = kwargs.get("tilt_position", 100)
            self._current_cover_tilt_position = tilt_position
            if self._reversed_tilt:
                tilt_position = 100 - tilt_position
            tilt_position = int(tilt_position * 90 / 100)
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(9, {tilt_position})')"}
            self._last_command_time = self.hass.loop.time() if self.hass is not None else None
            self.async_write_ha_state()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to set the cover tilt position: {ex}")

    async def async_open_cover_tilt(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            tilt_value = 0 if self._reversed_tilt else 90
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(9, {tilt_value})')"}
            self._last_command_time = self.hass.loop.time() if self.hass is not None else None
            self.async_write_ha_state()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to open the cover tilt: {ex}")

    async def async_close_cover_tilt(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            tilt_value = 90 if self._reversed_tilt else 0
            command = {"command": f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:execute(9, {tilt_value})')"}
            self._last_command_time = self.hass.loop.time() if self.hass is not None else None
            self.async_write_ha_state()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to close the cover tilt: {ex}")

    async def async_update(self):
        if not self._initialized:
            return
        
        if self._last_command_time and self.hass.loop.time() - self._last_command_time < 2:
            return
            
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
                    position = data.get("status_2")
                    if self._reversed:
                        position = 100 - position
                    self._state = STATE_CLOSED if position == 0 else STATE_OPEN
                    if data.get("status") == 1:
                        self._state = STATE_OPENING
                    elif data.get("status") == 2:
                        self._state = STATE_CLOSING
                    self._current_cover_position = position
                    tilt_position = int(data.get("status_3") * 100 / 90)
                    if self._reversed_tilt:
                        tilt_position = 100 - tilt_position
                    self._current_cover_tilt_position = tilt_position
                    self.async_write_ha_state()
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to update the cover state: {ex}")
            self._state = None
