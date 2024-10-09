"""
==================================================
Author: Jan Nalepka
Version: 1.1
Date: 2024-05-17
Repository: https://github.com/jnalepka/GrentonObjects_HomeAssistant
==================================================
"""

import requests
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

DOMAIN = 'grenton_objects'

CONF_API_ENDPOINT = 'api_endpoint'
CONF_GRENTON_ID = 'grenton_id'
CONF_OBJECT_NAME = 'name'
CONF_REVERSED = 'reversed'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Required(CONF_REVERSED, default=False): bool,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Cover'): str
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_endpoint = config.get(CONF_API_ENDPOINT)
    grenton_id = config.get(CONF_GRENTON_ID)
    reversed = config.get(CONF_REVERSED)
    object_name = config.get(CONF_OBJECT_NAME)

    add_entities([GrentonCover(api_endpoint, grenton_id, reversed, object_name)], True)

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

    def open_cover(self, **kwargs):
        try:
            command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(0, 0)')"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            self._state = STATE_OPENING
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to open the cover: {ex}")

    def close_cover(self, **kwargs):
        try:
            command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(1, 0)')"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            self._state = STATE_CLOSING
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to close the cover: {ex}")

    def stop_cover(self, **kwargs):
        try:
            command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(3, 0)')"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            self._state = STATE_OPEN
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to stop the cover: {ex}")

    def set_cover_position(self, **kwargs):
        try:
            position = kwargs.get("position", 100)
            self._current_cover_position = position
            if self._reversed == True:
                position = 100 - position
            command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(10, {position})')"}
            if self._grenton_id.split('->')[1].startswith("ZWA"):
                command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(7, {position})')"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
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
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to set the cover position: {ex}")

    def set_cover_tilt_position(self, **kwargs):
        try:
            tilt_position = kwargs.get("tilt_position", 90)
            self._current_cover_tilt_position = tilt_position
            tilt_position = tilt_position * 90 / 100
            command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(9, {tilt_position})')"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to set the cover tilt position: {ex}")

    def open_cover_tilt(self, **kwargs):
        try:
            command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(9, 90)')"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to open the cover tilt: {ex}")

    def close_cover_tilt(self, **kwargs):
        try:
            command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(9, 0)')"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to close the cover tilt: {ex}")

    def update(self):
        try:
            if self._grenton_id.split('->')[1].startswith("ZWA"):
                command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(2)')"}
            else:
                command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(0)')"}
            if self._grenton_id.split('->')[1].startswith("ZWA"):
                command.update({"status_2": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(4)')"})
            else:
                command.update({"status_2": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(7)')"})
            if self._grenton_id.split('->')[1].startswith("ZWA"):
                command.update({"status_3": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(6)')"})
            else:
                command.update({"status_3": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(8)')"})
            response = requests.get(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            data = response.json()
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
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to update the cover state: {ex}")
            self._state = None
