"""
==================================================
Author: Jan Nalepka
Script version: 3.4
Date: 20.10.2025
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
    CONF_GRENTON_TYPE_DEFAULT_SENSOR,
    CONF_DEVICE_CLASS,
    CONF_STATE_CLASS,
    CONF_REVERSED,
    DEVICE_TYPE_OPTIONS,
    DEVICE_CLASS_OPTIONS,
    STATE_CLASS_OPTIONS,
    LIGHT_GRENTON_TYPE_OPTIONS,
    SENSOR_GRENTON_TYPE_OPTIONS,
    LIGHT_GRENTON_TYPE_LED,
    CONF_AUTO_UPDATE,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL
)
from .options_flow import GrentonOptionsFlowHandler
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig


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
                    vol.Required("device_type"): SelectSelector(
                        SelectSelectorConfig(
                            options=DEVICE_TYPE_OPTIONS,
                            translation_key="device_type"
                        )
                    )
                })
            )

        self.device_type = user_input["device_type"]
        if self.device_type == "light":
            return await self.async_step_light_config()
        elif self.device_type == "switch":
            return await self.async_step_switch_config()
        elif self.device_type == "cover":
            return await self.async_step_cover_config()
        elif self.device_type == "climate":
            return await self.async_step_climate_config()
        elif self.device_type == "sensor":
            return await self.async_step_sensor_config()
        elif self.device_type == "binary_sensor":
            return await self.async_step_binary_sensor_config()
        elif self.device_type == "button":
            return await self.async_step_button_config()
        
    def _persist_last_inputs(self, user_input: dict) -> None:
        self.hass.data[f"{DOMAIN}_last_api_endpoint"] = user_input[CONF_API_ENDPOINT]

        grenton_id = user_input.get(CONF_GRENTON_ID)
        if grenton_id and "->" in grenton_id:
            self.hass.data[f"{DOMAIN}_last_grenton_clu_id"] = grenton_id.split("->")[0]

    def _is_duplicate_grenton_id(self, grenton_id: str, grenton_type: str | None = None) -> bool:
        for entry in self._async_current_entries():
            existing_id = entry.data.get(CONF_GRENTON_ID)
            existing_type = entry.data.get(CONF_GRENTON_TYPE)

            if existing_id == grenton_id and existing_type == grenton_type:
                return True

            if grenton_type not in LIGHT_GRENTON_TYPE_LED and existing_id == grenton_id:
                return True

        return False

    async def async_step_light_config(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="light_config",
                data_schema=self._get_device_schema()
            )
        
        if self._is_duplicate_grenton_id(user_input[CONF_GRENTON_ID], user_input[CONF_GRENTON_TYPE]):
            return self.async_show_form(
                step_id="light_config",
                data_schema=self._get_device_schema(),
                errors={"base": "duplicate_grenton_id"}
            )

        self._persist_last_inputs(user_input)

        return self.async_create_entry(title=user_input[CONF_OBJECT_NAME], data={
            "device_type": self.device_type,
            CONF_API_ENDPOINT: user_input[CONF_API_ENDPOINT],
            CONF_GRENTON_ID: user_input[CONF_GRENTON_ID],
            CONF_OBJECT_NAME: user_input[CONF_OBJECT_NAME],
            CONF_GRENTON_TYPE: user_input[CONF_GRENTON_TYPE],
            CONF_AUTO_UPDATE: user_input[CONF_AUTO_UPDATE],
            CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL]
        })
    
    async def async_step_switch_config(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="switch_config",
                data_schema=self._get_device_schema()
            )
        
        if self._is_duplicate_grenton_id(user_input[CONF_GRENTON_ID]):
            return self.async_show_form(
                step_id="switch_config",
                data_schema=self._get_device_schema(),
                errors={"base": "duplicate_grenton_id"}
            )

        self._persist_last_inputs(user_input)

        return self.async_create_entry(title=user_input[CONF_OBJECT_NAME], data={
            "device_type": self.device_type,
            CONF_API_ENDPOINT: user_input[CONF_API_ENDPOINT],
            CONF_GRENTON_ID: user_input[CONF_GRENTON_ID],
            CONF_OBJECT_NAME: user_input[CONF_OBJECT_NAME],
            CONF_AUTO_UPDATE: user_input[CONF_AUTO_UPDATE],
            CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL]
        })
    
    async def async_step_cover_config(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="cover_config",
                data_schema=self._get_device_schema()
            )
        
        if self._is_duplicate_grenton_id(user_input[CONF_GRENTON_ID]):
            return self.async_show_form(
                step_id="cover_config",
                data_schema=self._get_device_schema(),
                errors={"base": "duplicate_grenton_id"}
            )

        self._persist_last_inputs(user_input)

        return self.async_create_entry(title=user_input[CONF_OBJECT_NAME], data={
            "device_type": self.device_type,
            CONF_API_ENDPOINT: user_input[CONF_API_ENDPOINT],
            CONF_GRENTON_ID: user_input[CONF_GRENTON_ID],
            CONF_OBJECT_NAME: user_input[CONF_OBJECT_NAME],
            CONF_REVERSED: user_input[CONF_REVERSED],
            CONF_AUTO_UPDATE: user_input[CONF_AUTO_UPDATE],
            CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL]
        })
    
    async def async_step_climate_config(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="climate_config",
                data_schema=self._get_device_schema()
            )
        
        if self._is_duplicate_grenton_id(user_input[CONF_GRENTON_ID]):
            return self.async_show_form(
                step_id="climate_config",
                data_schema=self._get_device_schema(),
                errors={"base": "duplicate_grenton_id"}
            )

        self._persist_last_inputs(user_input)

        return self.async_create_entry(title=user_input[CONF_OBJECT_NAME], data={
            "device_type": self.device_type,
            CONF_API_ENDPOINT: user_input[CONF_API_ENDPOINT],
            CONF_GRENTON_ID: user_input[CONF_GRENTON_ID],
            CONF_OBJECT_NAME: user_input[CONF_OBJECT_NAME],
            CONF_AUTO_UPDATE: user_input[CONF_AUTO_UPDATE],
            CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL]
        })
    
    async def async_step_sensor_config(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="sensor_config",
                data_schema=self._get_device_schema()
            )
        
        if self._is_duplicate_grenton_id(user_input[CONF_GRENTON_ID]):
            return self.async_show_form(
                step_id="sensor_config",
                data_schema=self._get_device_schema(),
                errors={"base": "duplicate_grenton_id"}
            )

        self._persist_last_inputs(user_input)

        return self.async_create_entry(title=user_input[CONF_OBJECT_NAME], data={
            "device_type": self.device_type,
            CONF_API_ENDPOINT: user_input[CONF_API_ENDPOINT],
            CONF_GRENTON_ID: user_input[CONF_GRENTON_ID],
            CONF_OBJECT_NAME: user_input[CONF_OBJECT_NAME],
            CONF_GRENTON_TYPE: user_input[CONF_GRENTON_TYPE],
            CONF_DEVICE_CLASS: user_input[CONF_DEVICE_CLASS],
            CONF_STATE_CLASS: user_input[CONF_STATE_CLASS],
            CONF_AUTO_UPDATE: user_input[CONF_AUTO_UPDATE],
            CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL]
        })
    
    async def async_step_binary_sensor_config(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="binary_sensor_config",
                data_schema=self._get_device_schema()
            )
        
        if self._is_duplicate_grenton_id(user_input[CONF_GRENTON_ID]):
            return self.async_show_form(
                step_id="binary_sensor_config",
                data_schema=self._get_device_schema(),
                errors={"base": "duplicate_grenton_id"}
            )

        self._persist_last_inputs(user_input)

        return self.async_create_entry(title=user_input[CONF_OBJECT_NAME], data={
            "device_type": self.device_type,
            CONF_API_ENDPOINT: user_input[CONF_API_ENDPOINT],
            CONF_GRENTON_ID: user_input[CONF_GRENTON_ID],
            CONF_OBJECT_NAME: user_input[CONF_OBJECT_NAME],
            CONF_AUTO_UPDATE: user_input[CONF_AUTO_UPDATE],
            CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL]
        })
    
    async def async_step_button_config(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="button_config",
                data_schema=self._get_device_schema()
            )
        
        if self._is_duplicate_grenton_id(user_input[CONF_GRENTON_ID]):
            return self.async_show_form(
                step_id="button_config",
                data_schema=self._get_device_schema(),
                errors={"base": "duplicate_grenton_id"}
            )

        self._persist_last_inputs(user_input)

        return self.async_create_entry(title=user_input[CONF_OBJECT_NAME], data={
            "device_type": self.device_type,
            CONF_API_ENDPOINT: user_input[CONF_API_ENDPOINT],
            CONF_GRENTON_ID: user_input[CONF_GRENTON_ID],
            CONF_OBJECT_NAME: user_input[CONF_OBJECT_NAME]
        })
        
    def _get_device_schema(self):
        last_api_endpoint = self.hass.data.get(f"{DOMAIN}_last_api_endpoint", "http://192.168.0.4/HAlistener")
        last_grenton_clu_id = self.hass.data.get(f"{DOMAIN}_last_grenton_clu_id", "CLU220000000")
        if self.device_type == "light":
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->DOU0000"): str,
                vol.Required(CONF_GRENTON_TYPE, default=CONF_GRENTON_TYPE_DOUT): vol.In(LIGHT_GRENTON_TYPE_OPTIONS),
                vol.Required(CONF_AUTO_UPDATE, default=True): bool,
                vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600))
            })
        elif self.device_type == "switch":
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->DOU0000"): str,
                vol.Required(CONF_AUTO_UPDATE, default=True): bool,
                vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600))
            })
        elif self.device_type == "cover":
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->ROL0000"): str,
                vol.Required(CONF_REVERSED, default=False): bool,
                vol.Required(CONF_AUTO_UPDATE, default=True): bool,
                vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600))
            })
        elif self.device_type == "climate":
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->THE0000"): str,
                vol.Required(CONF_AUTO_UPDATE, default=True): bool,
                vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600))
            })
        elif self.device_type == "sensor":
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->PAN0000"): str,
                vol.Required(CONF_GRENTON_TYPE, default=CONF_GRENTON_TYPE_DEFAULT_SENSOR): vol.In(SENSOR_GRENTON_TYPE_OPTIONS),
                vol.Required(CONF_DEVICE_CLASS, default="temperature"): vol.In(DEVICE_CLASS_OPTIONS),
                vol.Required(CONF_DEVICE_CLASS, default="temperature"): SelectSelector(
                    SelectSelectorConfig(
                        options=DEVICE_CLASS_OPTIONS,
                        translation_key="device_class"
                    )
                ),
                vol.Required(CONF_STATE_CLASS, default="measurement"): SelectSelector(
                    SelectSelectorConfig(
                        options=STATE_CLASS_OPTIONS,
                        translation_key="state_class"
                    )
                ),
                vol.Required(CONF_AUTO_UPDATE, default=True): bool,
                vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600))
            })
        elif self.device_type == "binary_sensor":
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->DIN0000"): str,
                vol.Required(CONF_AUTO_UPDATE, default=True): bool,
                vol.Required(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600))
            })
        elif self.device_type == "button":
            return vol.Schema({
                vol.Required(CONF_OBJECT_NAME): str,
                vol.Required(CONF_API_ENDPOINT, default=last_api_endpoint): str,
                vol.Required(CONF_GRENTON_ID, default=last_grenton_clu_id+"->script_name"): str
            })
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> GrentonOptionsFlowHandler:
        return GrentonOptionsFlowHandler(config_entry)