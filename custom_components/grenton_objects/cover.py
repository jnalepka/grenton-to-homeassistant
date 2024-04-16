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

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Cover'): str
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_endpoint = config.get(CONF_API_ENDPOINT)
    grenton_id = config.get(CONF_GRENTON_ID)
    object_name = config.get(CONF_OBJECT_NAME)

    add_entities([GrentonCover(api_endpoint, grenton_id, object_name)], True)

class GrentonCover(CoverEntity):
    def __init__(self, api_endpoint, grenton_id, object_name):
        self._device_class = CoverDeviceClass.BLIND
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._object_name = object_name
        self._state = None
        self._current_cover_position = None
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

    def open_cover(self, **kwargs):
        try:
            command = {"command": f"{self._grenton_id}:execute(0, 0)"}
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
            command = {"command": f"{self._grenton_id}:execute(1, 0)"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            self._state = STATE_CLOSING
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to open the cover: {ex}")

    def stop_cover(self, **kwargs):
        try:
            command = {"command": f"{self._grenton_id}:execute(3, 0)"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            self._state = STATE_OPEN
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to open the cover: {ex}")

    def set_cover_position(self, **kwargs):
        try:
            position = kwargs.get("position", 100)
            command = {"command": f"{self._grenton_id}:execute(10, {position})"}
            response = requests.post(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            if (position > self._current_cover_position):
                self._state = STATE_OPENING
            else:
                self._state = STATE_CLOSING
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to open the cover: {ex}")

    def update(self):
        try:
            command = {"status": f"{self._grenton_id}:get(0)"} # state
            command.update({"status_2": f"{self._grenton_id}:get(7)"}) # position
            response = requests.get(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            data = response.json()
            self._state = STATE_CLOSED if data.get("object_value_2") == 0 else STATE_OPEN
            if data.get("object_value") == 1:
                self._state = STATE_OPENING
            elif data.get("object_value") == 2:
                self._state = STATE_CLOSING
            self._current_cover_position = data.get("object_value_2")
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to update the light state: {ex}")
            self._state = None
