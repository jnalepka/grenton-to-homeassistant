import requests
import logging
import json
import voluptuous as vol
from homeassistant.components.sensor import (
    SensorEntity,
    PLATFORM_SCHEMA
)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'grenton_objects'

CONF_API_ENDPOINT = 'api_endpoint'
CONF_GRENTON_ID = 'grenton_id'
CONF_GRENTON_TYPE = 'grenton_type'
CONF_OBJECT_NAME = 'name'
CONF_UNIT_OF_MEASUREMENT = 'unit_of_measurement'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Required(CONF_GRENTON_TYPE, default='UNKNOWN'): str, #MODBUS_RTU, MODBUS_VALUE, MODBUS, MODBUS_CLIENT, MODBUS_SLAVE_RTU
    vol.Required(CONF_UNIT_OF_MEASUREMENT, default='°C'): str,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Sensor'): str
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_endpoint = config.get(CONF_API_ENDPOINT)
    grenton_id = config.get(CONF_GRENTON_ID)
    grenton_type = config.get(CONF_GRENTON_TYPE)
    object_name = config.get(CONF_OBJECT_NAME)
    unit_of_measurement = config.get(CONF_UNIT_OF_MEASUREMENT)

    add_entities([GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement)], True)

class GrentonSensor(SensorEntity):
    def __init__(self, api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement):
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._grenton_type = grenton_type
        self._object_name = object_name
        self._unique_id = f"grenton_{grenton_id.split('->')[1]}"
        self._native_value = None
        self._native_unit_of_measurement = unit_of_measurement

    @property
    def name(self):
        return self._object_name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def native_value(self):
        return self._native_value
    
    @property
    def native_unit_of_measurement(self):
        return self._native_unit_of_measurement

    def update(self):
        try:
            if self._grenton_id.split('->')[1].isupper():
                grenton_type_mapping = {
                    "MODBUS": 14,
                    "MODBUS_VALUE": 20,
                    "MODBUS_RTU": 22,
                    "MODBUS_CLIENT": 19,
                    "MODBUS_SERVER": 10,
                    "MODBUS_SLAVE_RTU": 10,
                }
                index = grenton_type_mapping.get(self._grenton_type, 0)
                command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get({index})')"}
            else:
                command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, 'getVar(\"{self._grenton_id.split('->')[1]}\")')"}
            response = requests.get(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            data = response.json()
            self._native_value = data.get("status")
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to update the switch state: {ex}")
            self._state = None
