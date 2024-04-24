import requests
import logging
import json
import voluptuous as vol
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    PLATFORM_SCHEMA
)
from homeassistant.const import (STATE_ON, STATE_OFF)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'grenton_objects'

CONF_API_ENDPOINT = 'api_endpoint'
CONF_GRENTON_ID = 'grenton_id'
CONF_OBJECT_NAME = 'name'
CONF_SENSOR_TYPE = 'sensor_type'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Binary Sensor'): str,
    vol.Required(CONF_SENSOR_TYPE, default='LOCK'): str, #all from BinarySensorDeviceClass
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_endpoint = config.get(CONF_API_ENDPOINT)
    grenton_id = config.get(CONF_GRENTON_ID)
    object_name = config.get(CONF_OBJECT_NAME)
    sensor_type = config.get(CONF_SENSOR_TYPE)

    add_entities([GrentonBinarySensor(api_endpoint, grenton_id, object_name, sensor_type)], True)

class GrentonBinarySensor(BinarySensorEntity):
    def __init__(self, api_endpoint, grenton_id, object_name, sensor_type):
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._object_name = object_name
        self._unique_id = f"grenton_{grenton_id.split('->')[1]}"
        self._state = None

        device_class_mapping = {
            "BATTERY": BinarySensorDeviceClass.BATTERY,
            "BATTERY_CHARGING": BinarySensorDeviceClass.BATTERY_CHARGING,
            "CO": BinarySensorDeviceClass.CO,
            "COLD": BinarySensorDeviceClass.COLD,
            "CONNECTIVITY": BinarySensorDeviceClass.CONNECTIVITY,
            "DOOR": BinarySensorDeviceClass.DOOR,
            "GARAGE_DOOR": BinarySensorDeviceClass.GARAGE_DOOR,
            "GAS": BinarySensorDeviceClass.GAS,
            "HEAT": BinarySensorDeviceClass.HEAT,
            "LIGHT": BinarySensorDeviceClass.LIGHT,
            "LOCK": BinarySensorDeviceClass.LOCK,
            "MOISTURE": BinarySensorDeviceClass.MOISTURE,
            "MOTION": BinarySensorDeviceClass.MOTION,
            "MOVING": BinarySensorDeviceClass.MOVING,
            "OCCUPANCY": BinarySensorDeviceClass.OCCUPANCY,
            "OPENING": BinarySensorDeviceClass.OPENING,
            "PLUG": BinarySensorDeviceClass.PLUG,
            "POWER": BinarySensorDeviceClass.POWER,
            "PRESENCE": BinarySensorDeviceClass.PRESENCE,
            "PROBLEM": BinarySensorDeviceClass.PROBLEM,
            "RUNNING": BinarySensorDeviceClass.RUNNING,
            "SAFETY": BinarySensorDeviceClass.SAFETY,
            "SMOKE": BinarySensorDeviceClass.SMOKE,
            "SOUND": BinarySensorDeviceClass.SOUND,
            "TAMPER": BinarySensorDeviceClass.TAMPER,
            "UPDATE": BinarySensorDeviceClass.UPDATE,
            "VIBRATION": BinarySensorDeviceClass.VIBRATION,
            "WINDOW": BinarySensorDeviceClass.WINDOW
        }
        self._device_class = device_class_mapping.get(sensor_type.upper(), BinarySensorDeviceClass.LOCK)

    @property
    def name(self):
        return self._object_name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def is_on(self):
        return self._state == STATE_ON

    def update(self):
        try:
            command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(0)')"}
            response = requests.get(
                f"{self._api_endpoint}",
                json = command
            )
            response.raise_for_status()
            data = response.json()
            self._state = STATE_OFF if data.get("status") == 0 else STATE_ON
        except requests.RequestException as ex:
            _LOGGER.error(f"Failed to update the switch state: {ex}")
            self._state = None
