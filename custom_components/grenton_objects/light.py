import requests
import logging
import json
import voluptuous as vol
from homeassistant.components.light import LightEntity, PLATFORM_SCHEMA
from homeassistant.const import (STATE_ON, STATE_OFF)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'grenton_objects'

CONF_API_ENDPOINT = 'api_endpoint'
CONF_LIGHT_ID = 'grenton_id'
CONF_LIGHT_NAME = 'name'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_LIGHT_ID): str,
    vol.Optional(CONF_LIGHT_NAME, default='Grenton Light'): str,
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

    @property
    def name(self):
        return self._light_name

    @property
    def is_on(self):
        return self._state == STATE_ON

    def turn_on(self, **kwargs):
        try:
            response = requests.post(
                f"{self._api_endpoint}/HAlistener2",
                json = {"command": f"{self._light_id}:execute(1, 0)"} # on
            ) 
            response.raise_for_status()
            self._state = STATE_ON
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to turn on the light: {ex}")

    def turn_off(self, **kwargs):
        try:
            response = requests.post(
                f"{self._api_endpoint}/HAlistener2",
                json = {"command": f"{self._light_id}:execute(2, 0)"} # off
            )
            response.raise_for_status()
            self._state = STATE_OFF
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to turn off the light: {ex}")

    def update(self):
        try:
            response = requests.get(
                f"{self._api_endpoint}/HAlistener2",
                json = {"status": f"{self._light_id}:get(0)"} # get device value
            )
            response.raise_for_status()
            data = response.json()
            self._state = STATE_OFF if data.get("object_value") == 0 else STATE_ON
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to update the light state: {ex}")
            self._state = None
