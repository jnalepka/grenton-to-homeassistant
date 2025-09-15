"""
==================================================
Author: Jan Nalepka
Script version: 3.0
Date: 15.09.2025
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import (
    DOMAIN,
    CONF_API_ENDPOINT,
    CONF_GRENTON_ID,
    CONF_OBJECT_NAME,
    CONF_GRENTON_TYPE,
    CONF_GRENTON_TYPE_DOUT,
    CONF_GRENTON_TYPE_DIMMER,
    CONF_GRENTON_TYPE_RGB,
    CONF_GRENTON_TYPE_LED_R,
    CONF_GRENTON_TYPE_LED_G,
    CONF_GRENTON_TYPE_LED_B,
    CONF_GRENTON_TYPE_LED_W,
    CONF_GRENTON_TYPE_DEFAULT_SENSOR,
    CONF_GRENTON_TYPE_MODBUS_RTU,
    CONF_GRENTON_TYPE_MODBUS_VALUE,
    CONF_GRENTON_TYPE_MODBUS,
    CONF_GRENTON_TYPE_MODBUS_CLIENT,
    CONF_GRENTON_TYPE_MODBUS_SERVER,
    CONF_GRENTON_TYPE_MODBUS_SLAVE_RTU,
    CONF_DEVICE_CLASS,
    CONF_STATE_CLASS,
    CONF_REVERSED,
    CONF_DEVICE_TYPE,
    CONF_DEVICE_TYPE_LIGHT,
    CONF_DEVICE_TYPE_SWITCH,
    CONF_DEVICE_TYPE_COVER,
    CONF_DEVICE_TYPE_CLIMATE,
    CONF_DEVICE_TYPE_SENSOR,
    CONF_DEVICE_TYPE_BINARY_SENSOR,
    CONF_DEVICE_TYPE_BUTTON
)
import logging
from .options_flow import GrentonOptionsFlowHandler

_LOGGER = logging.getLogger(__name__)

DEVICE_TYPES = {
    CONF_DEVICE_TYPE_LIGHT: "Light",
    CONF_DEVICE_TYPE_SWITCH: "Switch",
    CONF_DEVICE_TYPE_COVER: "Cover",
    CONF_DEVICE_TYPE_CLIMATE: "Climate",
    CONF_DEVICE_TYPE_SENSOR: "Sensor",
    CONF_DEVICE_TYPE_BINARY_SENSOR: "Binary sensor",
    CONF_DEVICE_TYPE_BUTTON: "Script"
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
                    vol.Required(CONF_DEVICE_TYPE): vol.In(DEVICE_TYPES)
                })
            )

        self.device_type = user_input[CONF_DEVICE_TYPE]
        return await self.async_step_device_config()

    async def async_step_device_config(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="device_config",
                data_schema=self._get_device_schema()
            )

        self.hass.data[f"{DOMAIN}_last_api_endpoint"] = user_input[CONF_API_ENDPOINT]
        self.hass.data[f"{DOMAIN}_last_grenton_clu_id"] = user_input[CONF_GRENTON_ID].split("->")[0]

        return self.async_create_entry(title=user_input[CONF_OBJECT_NAME], data={
            CONF_DEVICE_TYPE: self.device_type,
            CONF_API_ENDPOINT: user_input[CONF_API_ENDPOINT],
            CONF_GRENTON_ID: user_input[CONF_GRENTON_ID],
            CONF_OBJECT_NAME: user_input[CONF_OBJECT_NAME],
            CONF_GRENTON_TYPE: user_input.get(CONF_GRENTON_TYPE, None),
            CONF_DEVICE_CLASS: user_input.get(CONF_DEVICE_CLASS, None),
            CONF_STATE_CLASS: user_input.get(CONF_STATE_CLASS, None),
            CONF_REVERSED: user_input.get(CONF_REVERSED, None)
        })
        
    def _get_device_schema(self):
        last_api_endpoint = self.hass.data.get(f"{DOMAIN}_last_api_endpoint", "http://192.168.0.4/HAlistener")
        last_grenton_clu_id = self.hass.data.get(f"{DOMAIN}_last_grenton_clu_id", "CLU220000000")
        if self.device_type == CONF_DEVICE_TYPE_LIGHT:
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->DOU0000"): str,
                vol.Required(CONF_GRENTON_TYPE, default=CONF_GRENTON_TYPE_DOUT): vol.In([CONF_GRENTON_TYPE_DOUT, CONF_GRENTON_TYPE_DIMMER, CONF_GRENTON_TYPE_RGB, CONF_GRENTON_TYPE_LED_R, CONF_GRENTON_TYPE_LED_G, CONF_GRENTON_TYPE_LED_B, CONF_GRENTON_TYPE_LED_W]),
            })
        elif self.device_type == CONF_DEVICE_TYPE_SWITCH:
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->DOU0000"): str,
            })
        elif self.device_type == CONF_DEVICE_TYPE_COVER:
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->ROL0000"): str,
                vol.Optional(CONF_REVERSED, default=False): bool,
            })
        elif self.device_type == CONF_DEVICE_TYPE_CLIMATE:
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->THE0000"): str,
            })
        elif self.device_type == CONF_DEVICE_TYPE_SENSOR:
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->PAN0000"): str,
                vol.Optional(CONF_GRENTON_TYPE, default=CONF_GRENTON_TYPE_DEFAULT_SENSOR): vol.In([CONF_GRENTON_TYPE_DEFAULT_SENSOR, CONF_GRENTON_TYPE_MODBUS_RTU, CONF_GRENTON_TYPE_MODBUS_VALUE, CONF_GRENTON_TYPE_MODBUS, CONF_GRENTON_TYPE_MODBUS_CLIENT, CONF_GRENTON_TYPE_MODBUS_SERVER, CONF_GRENTON_TYPE_MODBUS_SLAVE_RTU]),
                vol.Optional(CONF_DEVICE_CLASS, default="temperature"): vol.In([
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
                vol.Optional(CONF_STATE_CLASS, default="measurement"): vol.In(["measurement", "total", "total_increasing"])
            })
        elif self.device_type == CONF_DEVICE_TYPE_BINARY_SENSOR:
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->DIN0000"): str
            })
        elif self.device_type == CONF_DEVICE_TYPE_BUTTON:
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default="script_name (script on GateHTTP) or "+last_grenton_clu_id+"->script_name"): str
            })
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> GrentonOptionsFlowHandler:
        return GrentonOptionsFlowHandler()