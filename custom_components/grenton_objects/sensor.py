"""
==================================================
Author: Jan Nalepka
Version: 2.1.0
Date: 2024-11-27
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import aiohttp
from .const import DOMAIN
import logging
import json
import voluptuous as vol
from homeassistant.components.sensor import (
    SensorEntity,
    PLATFORM_SCHEMA
)

from homeassistant.const import UnitOfTemperature

_LOGGER = logging.getLogger(__name__)

CONF_API_ENDPOINT = 'api_endpoint'
CONF_GRENTON_ID = 'grenton_id'
CONF_GRENTON_TYPE = 'grenton_type'
CONF_OBJECT_NAME = 'name'
CONF_DEVICE_CLASS = 'device_class'
CONF_STATE_CLASS = 'state_class'
CONF_UNIT_OF_MEASUREMENT = 'unit_of_measurement'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Required(CONF_GRENTON_TYPE, default='DEFAULT_SENSOR'): str, #DEFAULT_SENSOR, MODBUS_RTU, MODBUS_VALUE, MODBUS, MODBUS_CLIENT, MODBUS_SLAVE_RTU
    vol.Required(CONF_UNIT_OF_MEASUREMENT, default=UnitOfTemperature.CELSIUS): str,
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Sensor'): str,
    vol.Optional(CONF_DEVICE_CLASS, default=''): str,
    vol.Optional(CONF_STATE_CLASS, default=''): str
})

DEFAULT_UNITS = {
    'apparent_power': 'VA',
    'atmospheric_pressure': 'hPa',
    'battery': '%',
    'carbon_dioxide': 'ppm',
    'carbon_monoxide': 'ppm',
    'current': 'mA',
    'distance': 'm',
    'duration': 'ms',
    'energy': 'kWh',
    'energy_storage': 'kWh',
    'frequency': 'Hz',
    'gas': 'm³',
    'humidity': '%',
    'illuminance': 'lx',
    'irradiance': 'W/m²',
    'moisture': '%',
    'nitrogen_dioxide': 'µg/m³',
    'nitrogen_monoxide': 'µg/m³',
    'nitrous_oxide': 'µg/m³',
    'ozone': 'µg/m³',
    'ph': None,
    'pm1': 'µg/m³',
    'pm10': 'µg/m³',
    'm25': 'µg/m³',
    'power': 'W',
    'power_factor': '%',
    'precipitation': 'cm',
    'precipitation_intensity': 'in/d',
    'pressure': 'hPa',
    'reactive_power': 'var',
    'signal_strength': 'dB',
    'sound_pressure': 'dB',
    'speed': 'm/s',
    'sulphur_dioxide': 'µg/m³',
    'temperature': '°C',
    'volatile_organic_compounds': 'µg/m³',
    'volatile_organic_compounds_parts': 'ppb',
    'voltage': 'V',
    'volume': 'L',
    'volume_flow_rate': 'm³/h',
    'volume_storage': 'L',
    'water': 'L',
    'weight': 'kg',
    'wind_speed': 'km/h'
}
    
async def async_setup_entry(hass, config_entry, async_add_entities):
    device = config_entry.data

    api_endpoint = device.get(CONF_API_ENDPOINT)
    grenton_id = device.get(CONF_GRENTON_ID)
    grenton_type = device.get(CONF_GRENTON_TYPE)
    object_name = device.get(CONF_OBJECT_NAME)
    device_class = device.get(CONF_DEVICE_CLASS)
    unit_of_measurement = DEFAULT_UNITS.get(device_class, None)
    state_class = device.get(CONF_STATE_CLASS)
    
    async_add_entities([GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class)], True)
    
    
class GrentonSensor(SensorEntity):
    def __init__(self, api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class):
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        self._grenton_type = grenton_type
        self._object_name = object_name
        if len(self._grenton_id.split('->')) == 1:
            self._unique_id = f"grenton_{grenton_id}"
        else:
            self._unique_id = f"grenton_{grenton_id.split('->')[1]}"
        self._native_value = None
        self._native_unit_of_measurement = unit_of_measurement
        self._device_class = device_class
        self._state_class = state_class

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

    @property
    def device_class(self):
        return self._device_class
    
    @property
    def state_class(self):
        return self._state_class

    async def async_update(self):
        try:
            if len(self._grenton_id.split('->')) == 1:
                command = {"status": f"return getVar(\"{self._grenton_id}\")"}
            elif self._grenton_id.split('->')[1].isupper():
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
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self._native_value = data.get("status")
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to update the switch state: {ex}")
            self._state = None
