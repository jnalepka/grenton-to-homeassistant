import requests
import logging
import json
import voluptuous as vol
from homeassistant.components.light import LightEntity, PLATFORM_SCHEMA, ColorMode
from homeassistant.const import (STATE_ON, STATE_OFF)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'grenton_objects'

CONF_API_ENDPOINT = 'api_endpoint'
CONF_LIGHT_ID = 'grenton_id'
CONF_LIGHT_NAME = 'name'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_LIGHT_ID): str,
    vol.Optional(CONF_LIGHT_NAME, default='Grenton Light'): str
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_endpoint = config.get(CONF_API_ENDPOINT)
    light_id = config.get(CONF_LIGHT_ID)
    light_name = config.get(CONF_LIGHT_NAME)

    add_entities([GrentonLight(api_endpoint, light_id, light_name)], True)

class GrentonLight(LightEntity):
    def __init__(self, api_endpoint, light_id, light_name):
        self._api_endpoint = api_endpoint
        self._light_id = light_id
        self._light_name = light_name
        self._state = None
        self._unique_id = f"grenton_{light_id.split('->')[1]}"
        self._brightness = None

        if light_id.split('->')[1].startswith("DIM"):
            self._supported_color_modes = [ColorMode.BRIGHTNESS]
        else:
            self._supported_color_modes = [ColorMode.ONOFF]


    @property
    def name(self):
        return self._light_name

    @property
    def is_on(self):
        return self._state == STATE_ON

    @property
    def supported_color_modes(self):
        return self._supported_color_modes

    @property
    def color_mode(self):
        return self._color_mode
    
    @property
    def color_mode(self) -> ColorMode:
        if (self._light_id.split('->')[1].startswith("DIM")):
            return ColorMode.BRIGHTNESS
        else:
            return ColorMode.ONOFF

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def brightness(self):
        return self._brightness

    def turn_on(self, **kwargs):
        try:
            response = requests.post(
                f"{self._api_endpoint}",
                json = {"command": f"{self._light_id}:set(0, 1)"}
            ) 
            response.raise_for_status()
            self._state = STATE_ON
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to turn on the light: {ex}")

    def turn_off(self, **kwargs):
        try:
            response = requests.post(
                f"{self._api_endpoint}",
                json = {"command": f"{self._light_id}:set(0, 0)"}
            )
            response.raise_for_status()
            self._state = STATE_OFF
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to turn off the light: {ex}")

    def update(self):
        try:
            response = requests.get(
                f"{self._api_endpoint}",
                json = {"status": f"{self._light_id}:get(0)"}
            )
            response.raise_for_status()
            data = response.json()
            self._state = STATE_OFF if data.get("object_value") == 0 else STATE_ON
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to update the light state: {ex}")
            self._state = None
