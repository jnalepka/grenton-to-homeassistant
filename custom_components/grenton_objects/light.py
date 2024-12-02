"""
==================================================
Author: Jan Nalepka
Version: 2.2.0
Date: 2024-12-01
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

import aiohttp
from .const import (
    DOMAIN,
    CONF_API_ENDPOINT,
    CONF_GRENTON_ID,
    CONF_OBJECT_NAME,
    CONF_GRENTON_TYPE,
    CONF_GRENTON_TYPE_UNKNOWN,
    CONF_GRENTON_TYPE_DIMMER,
    CONF_GRENTON_TYPE_RGB,
    CONF_GRENTON_TYPE_DOUT,
    CONF_GRENTON_TYPE_LED_R,
    CONF_GRENTON_TYPE_LED_G,
    CONF_GRENTON_TYPE_LED_B,
    CONF_GRENTON_TYPE_LED_W
)
import logging
import json
import voluptuous as vol
from homeassistant.components.light import (
    LightEntity, 
    PLATFORM_SCHEMA, 
    ColorMode
)
from homeassistant.const import (STATE_ON, STATE_OFF)
from homeassistant.util import color as color_util

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Required(CONF_GRENTON_TYPE, default=CONF_GRENTON_TYPE_UNKNOWN): str, #DOUT, DIMMER, RGB, LED_R, LED_G, LED_B, LED_W
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Light'): str
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    device = config_entry.data
    
    api_endpoint = device.get(CONF_API_ENDPOINT)
    grenton_id = device.get(CONF_GRENTON_ID)
    grenton_type = device.get(CONF_GRENTON_TYPE, CONF_GRENTON_TYPE_UNKNOWN)
    object_name = device.get(CONF_OBJECT_NAME, "Grenton Light")
    
    async_add_entities([GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)], True)

class GrentonLight(LightEntity):
    def __init__(self, api_endpoint, grenton_id, grenton_type, object_name):
        self._grenton_id = grenton_id
        self._api_endpoint = api_endpoint
        self._grenton_type = grenton_type
        self._object_name = object_name
        self._state = None
        self._supported_color_modes: set[ColorMode | str] = set()
        self._brightness = None
        self._rgb_color = None
        
        grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
        
        led_types = {
            CONF_GRENTON_TYPE_LED_R,
            CONF_GRENTON_TYPE_LED_G,
            CONF_GRENTON_TYPE_LED_B,
            CONF_GRENTON_TYPE_LED_W
        }
        
        if self._grenton_type in led_types:
            self._unique_id = f"grenton_{grenton_id_part_1}_{grenton_type}"
        else:
            self._unique_id = f"grenton_{grenton_id_part_1}"
    
        
        if grenton_type == CONF_GRENTON_TYPE_UNKNOWN:
            if grenton_id_part_1.startswith("DIM"):
                self._grenton_type = CONF_GRENTON_TYPE_DIMMER
            elif grenton_id_part_1.startswith("LED"):
                self._grenton_type = CONF_GRENTON_TYPE_RGB
            else:
                self._grenton_type = CONF_GRENTON_TYPE_DOUT

        brightness_types = {
            CONF_GRENTON_TYPE_DIMMER,
            CONF_GRENTON_TYPE_LED_R,
            CONF_GRENTON_TYPE_LED_G,
            CONF_GRENTON_TYPE_LED_B,
            CONF_GRENTON_TYPE_LED_W
        }
        
        if self._grenton_type in brightness_types:
            self._supported_color_modes.add(ColorMode.BRIGHTNESS)
        elif self._grenton_type == CONF_GRENTON_TYPE_RGB:
            self._supported_color_modes.add(ColorMode.RGB)
        else:
            self._supported_color_modes.add(ColorMode.ONOFF)

    @property
    def name(self):
        return self._object_name

    @property
    def is_on(self):
        return self._state == STATE_ON

    @property
    def supported_color_modes(self):
        return self._supported_color_modes
    
    @property
    def color_mode(self) -> ColorMode:
        brightness_types = {
            CONF_GRENTON_TYPE_DIMMER,
            CONF_GRENTON_TYPE_LED_R,
            CONF_GRENTON_TYPE_LED_G,
            CONF_GRENTON_TYPE_LED_B,
            CONF_GRENTON_TYPE_LED_W
        }
        
        if self._grenton_type in brightness_types:
            return ColorMode.BRIGHTNESS
        elif self._grenton_type == CONF_GRENTON_TYPE_RGB:
            return ColorMode.RGB
        else:
            return ColorMode.ONOFF

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def brightness(self):
        return self._brightness

    @property
    def rgb_color(self):
        return self._rgb_color
        
    def _generate_command(self, command_type, grenton_id_part_0, grenton_id_part_1, action, xml_index, param):
        return {
            command_type: f"{grenton_id_part_0}:execute(0, '{grenton_id_part_1}:{action}({xml_index}, {param})')"
        }
        
    def _generate_get_command(self, command_type, grenton_id_part_0, grenton_id_part_1, action, xml_index):
        return {
            command_type: f"return {grenton_id_part_0}:execute(0, '{grenton_id_part_1}:{action}({xml_index})')"
        }
        
    async def async_turn_on(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            brightness = kwargs.get("brightness", 255)
            scaled_brightness = brightness / 255
            rgb_color = kwargs.get("rgb_color")
            command_brightness_mapping = {
                CONF_GRENTON_TYPE_DIMMER: {"action": "set", "index": 0, "param": scaled_brightness},
                CONF_GRENTON_TYPE_LED_R: {"action": "execute", "index": 3, "param": brightness},
                CONF_GRENTON_TYPE_LED_G: {"action": "execute", "index": 4, "param": brightness},
                CONF_GRENTON_TYPE_LED_B: {"action": "execute", "index": 5, "param": brightness},
                CONF_GRENTON_TYPE_LED_W: {"action": "execute", "index": 12, "param": brightness},
            }
            
            if self._grenton_type in command_brightness_mapping:
                if grenton_id_part_1.startswith("ZWA"):
                    command = self._generate_command("command", grenton_id_part_0, grenton_id_part_1, "execute", 0, brightness)
                else:
                    config = command_brightness_mapping[self._grenton_type]
                    command = self._generate_command("command", grenton_id_part_0, grenton_id_part_1, config["action"], config["index"], config["param"])
                self._brightness = brightness
            elif self._grenton_type == CONF_GRENTON_TYPE_RGB:
                if rgb_color:
                    hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_color)
                    hex_color = f'\\"{hex_color}\\"'
                    if grenton_id_part_1.startswith("ZWA"):
                        command = self._generate_command("command", grenton_id_part_0, grenton_id_part_1, "execute", 3, hex_color)
                    else:
                        command = self._generate_command("command", grenton_id_part_0, grenton_id_part_1, "execute", 6, hex_color)
                    self._rgb_color = rgb_color
                else:
                    command = self._generate_command("command", grenton_id_part_0, grenton_id_part_1, "execute", 0, scaled_brightness)
                    self._brightness = brightness
            else:
                command = self._generate_command("command", grenton_id_part_0, grenton_id_part_1, "set", 0, 1)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    self._state = STATE_ON
                    self._brightness = None
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to turn on the light: {ex}")
            
    async def async_turn_off(self, **kwargs):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            command_mapping = {
                CONF_GRENTON_TYPE_RGB: {"action": "execute", "index": 0},
                CONF_GRENTON_TYPE_DIMMER: {"action": "set", "index": 0},
                CONF_GRENTON_TYPE_DOUT: {"action": "set", "index": 0},
                CONF_GRENTON_TYPE_LED_R: {"action": "execute", "index": 3},
                CONF_GRENTON_TYPE_LED_G: {"action": "execute", "index": 4},
                CONF_GRENTON_TYPE_LED_B: {"action": "execute", "index": 5},
                CONF_GRENTON_TYPE_LED_W: {"action": "execute", "index": 12},
            }
            
            if self._grenton_type == CONF_GRENTON_TYPE_DIMMER and grenton_id_part_1.startswith("ZWA"):
                config = {"action": "execute", "index": 0}
            else:
                config = command_mapping.get(self._grenton_type, {"action": "set", "index": 0})
            
            command = self._generate_command("command", grenton_id_part_0, grenton_id_part_1, config["action"], config["index"], 0)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    self._state = STATE_OFF
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to turn off the light: {ex}")

    async def async_update(self):
        try:
            grenton_id_part_0, grenton_id_part_1 = self._grenton_id.split('->')
            xml_index__mapping = {
                CONF_GRENTON_TYPE_RGB: 0,
                CONF_GRENTON_TYPE_DOUT: 0,
                CONF_GRENTON_TYPE_DIMMER: 0,
                CONF_GRENTON_TYPE_LED_R: 3,
                CONF_GRENTON_TYPE_LED_G: 4,
                CONF_GRENTON_TYPE_LED_B: 5,
                CONF_GRENTON_TYPE_LED_W: 15,
            }
            
            if self._grenton_type in xml_index__mapping:
                command = self._generate_get_command("status", grenton_id_part_0, grenton_id_part_1, "get", xml_index__mapping[self._grenton_type])
            else:
                command = self._generate_command("status", grenton_id_part_0, grenton_id_part_1, "get", 0)
            
            if self._grenton_type == CONF_GRENTON_TYPE_RGB:
                if grenton_id_part_1.startswith("ZWA"):
                    command.update(self._generate_command("status_2", grenton_id_part_0, grenton_id_part_1, "get", 3))
                else:
                    command.update(self._generate_command("status_2", grenton_id_part_0, grenton_id_part_1, "get", 6))

            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self._state = STATE_OFF if data.get("status") == 0 else STATE_ON
                    if self._grenton_type == CONF_GRENTON_TYPE_RGB or self._grenton_type == CONF_GRENTON_TYPE_DIMMER:
                        if self._grenton_type == CONF_GRENTON_TYPE_DIMMER and grenton_id_part_1.startswith("ZWA"):
                            self._brightness = data.get("status")
                        else:
                            self._brightness = data.get("status") * 255
                    elif self._grenton_type == CONF_GRENTON_TYPE_LED_R or self._grenton_type == CONF_GRENTON_TYPE_LED_G or self._grenton_type == CONF_GRENTON_TYPE_LED_B or self._grenton_type == CONF_GRENTON_TYPE_LED_W:
                        self._brightness = data.get("status")
                    
                    if self._grenton_type == CONF_GRENTON_TYPE_RGB:
                        self._rgb_color = color_util.rgb_hex_to_rgb_list(data.get("status_2").strip("#"))
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to update the light state: {ex}")
            self._state = None
