"""
==================================================
Author: Jan Nalepka
Version: 2.1.0
Date: 2024-11-27
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

DEVICE_TYPES = {
    "light": "Light",
    "switch": "Switch",
    "cover": "Cover",
    "climate": "Climate",
    "sensor": "Sensor",
    "binary_sensor": "Binary sensor"
}

class GrentonConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    def __init__(self):
        self.device_type = None
        self.device_class = None

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("device_type"): vol.In(DEVICE_TYPES)
                })
            )

        self.device_type = user_input["device_type"]
        return await self.async_step_device_config()

    async def async_step_device_config(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="device_config",
                data_schema=self._get_device_schema()
            )

        return self.async_create_entry(title=user_input["name"], data={
            "device_type": self.device_type,
            "api_endpoint": user_input["api_endpoint"],
            "grenton_id": user_input["grenton_id"],
            "name": user_input["name"],
            "grenton_type": user_input.get("grenton_type", None),
            "device_class": user_input.get("device_class", None),
            "state_class": user_input.get("state_class", None),
            "reversed": user_input.get("reversed", None)
        })
        
    def _get_device_schema(self):
        if self.device_type == "light":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id", default="CLU220000000->DOU0000"): str,
                vol.Required("grenton_type", default="DOUT"): vol.In(["DOUT","DIMMER", "RGB"]),
            })
        elif self.device_type == "switch":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id", default="CLU220000000->DOU0000"): str,
            })
        elif self.device_type == "cover":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id", default="CLU220000000->ROL0000"): str,
                vol.Optional("reversed", default=False): bool,
            })
        elif self.device_type == "climate":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id", default="CLU220000000->THE0000"): str,
            })
        elif self.device_type == "sensor":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id", default="CLU220000000->PAN0000"): str,
                vol.Optional("grenton_type", default="DEFAULT_SENSOR"): vol.In(["DEFAULT_SENSOR", "MODBUS_RTU", "MODBUS_VALUE", "MODBUS", "MODBUS_CLIENT", "MODBUS_SLAVE_RTU"]),
                vol.Optional("device_class", default="temperature"): vol.In([
                    "apparent_power",
                    "atmospheric_pressure",
                    "battery",
                    "carbon_dioxide",
                    "carbon_monoxide",
                    "current",
                    "distance",
                    "duration",
                    "energy",
                    "energy_storage",
                    "frequency",
                    "gas",
                    "humidity",
                    "illuminance",
                    "irradiance",
                    "moisture",
                    "nitrogen_dioxide",
                    "nitrogen_monoxide",
                    "nitrous_oxide",
                    "ozone",
                    "ph",
                    "pm1",
                    "pm10",
                    "pm25",
                    "power",
                    "power_factor",
                    "precipitation",
                    "precipitation_intensity",
                    "pressure",
                    "reactive_power",
                    "signal_strength",
                    "sound_pressure",
                    "speed",
                    "sulphur_dioxide",
                    "temperature",
                    "volatile_organic_compounds",
                    "volatile_organic_compounds_parts",
                    "voltage",
                    "volume",
                    "volume_flow_rate",
                    "volume_storage",
                    "water",
                    "weight",
                    "wind_speed"
                ]),
                vol.Optional("state_class", default="measurement"): vol.In(["measurement", "total", "total_increasing"])
            })
        elif self.device_type == "binary_sensor":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id", default="CLU220000000->DIN0000"): str
            })
