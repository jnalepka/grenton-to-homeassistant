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
from homeassistant.components.light import (
    LightEntity, 
    PLATFORM_SCHEMA, 
    ColorMode
)
from homeassistant.const import (STATE_ON, STATE_OFF)
from homeassistant.util import color as color_util

_LOGGER = logging.getLogger(__name__)

CONF_API_ENDPOINT = 'api_endpoint'
CONF_GRENTON_ID = 'grenton_id'
CONF_GRENTON_TYPE = 'grenton_type'
CONF_OBJECT_NAME = 'name'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_ENDPOINT): str,
    vol.Required(CONF_GRENTON_ID): str,
    vol.Required(CONF_GRENTON_TYPE, default='UNKNOWN'): str, #DOUT, DIMMER, RGB, LED_R, LED_G, LED_B, LED_W
    vol.Optional(CONF_OBJECT_NAME, default='Grenton Light'): str
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    device = config_entry.data
    
    api_endpoint = device.get(CONF_API_ENDPOINT)
    grenton_id = device.get(CONF_GRENTON_ID)
    grenton_type = device.get(CONF_GRENTON_TYPE, "UNKNOWN")
    object_name = device.get(CONF_OBJECT_NAME, "Grenton Light")
    
    async_add_entities([GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)], True)

class GrentonLight(LightEntity):
    def __init__(self, api_endpoint, grenton_id, grenton_type, object_name):
        self._api_endpoint = api_endpoint
        self._grenton_id = grenton_id
        if grenton_type == "DIMMER" or grenton_type == "LED_R" or grenton_type == "LED_G" or grenton_type == "LED_B" or grenton_type == "LED_W":
            self._unique_id = f"grenton_{grenton_id.split('->')[1]}{grenton_type}"
        else:
            self._unique_id = f"grenton_{grenton_id.split('->')[1]}" 
        self._object_name = object_name
        self._state = None
        self._unique_id = f"grenton_{grenton_id.split('->')[1]}"
        self._supported_color_modes: set[ColorMode | str] = set()
        self._brightness = None
        self._rgb_color = None

        if grenton_id.split('->')[1].startswith("DIM"):
            if grenton_type == "UNKNOWN": self._grenton_type = "DIMMER"
        elif grenton_id.split('->')[1].startswith("LED"):
            if grenton_type == "UNKNOWN": self._grenton_type = "RGB"
        else:
            if grenton_type == "UNKNOWN": self._grenton_type = "DOUT"

        if self._grenton_type == "DIMMER" or self._grenton_type == "LED_R" or self._grenton_type == "LED_G" or self._grenton_type == "LED_B" or self._grenton_type == "LED_W":
            self._supported_color_modes.add(ColorMode.BRIGHTNESS)
        elif self._grenton_type == "RGB":
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
        if self._grenton_type == "DIMMER" or self._grenton_type == "LED_R" or self._grenton_type == "LED_G" or self._grenton_type == "LED_B" or self._grenton_type == "LED_W":
            return ColorMode.BRIGHTNESS
        elif self._grenton_type == "RGB":
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

    async def async_turn_on(self, **kwargs):
        try:
            command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:set(0, 1)')"}
            if self._grenton_type == "DIMMER":
                brightness = kwargs.get("brightness", 255)
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(0, {brightness})')"}
                else:
                    scaled_brightness = brightness / 255
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:set(0, {scaled_brightness})')"}
                self._brightness = brightness
            elif self._grenton_type == "LED_R":
                brightness = kwargs.get("brightness", 255)
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(0, {brightness})')"}
                else:
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(3, {brightness})')"}
                self._brightness = brightness
            elif self._grenton_type == "LED_G":
                brightness = kwargs.get("brightness", 255)
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(0, {brightness})')"}
                else:
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(4, {brightness})')"}
                self._brightness = brightness
            elif self._grenton_type == "LED_B":
                brightness = kwargs.get("brightness", 255)
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(0, {brightness})')"}
                else:
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(5, {brightness})')"}
                self._brightness = brightness
            elif self._grenton_type == "LED_W":
                brightness = kwargs.get("brightness", 255)
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(0, {brightness})')"}
                else:
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(12, {brightness})')"}
                self._brightness = brightness
            elif self._grenton_type == "RGB":
                rgb_color = kwargs.get("rgb_color")
                if rgb_color:
                    hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_color)
                    if self._grenton_id.split('->')[1].startswith("ZWA"):
                        command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(3, \"{hex_color}\")')"}
                    else:
                        command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(6, \"{hex_color}\")')"}
                    self._rgb_color = rgb_color
                else:
                    brightness = kwargs.get("brightness", 255)
                    scaled_brightness = brightness / 255
                    command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(0, {scaled_brightness})')"}
                    self._brightness = brightness
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    self._state = STATE_ON
                    self._brightness = None
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to turn on the light: {ex}")
            
    async def async_turn_off(self, **kwargs):
        try:
            command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:set(0, 0)')"}
            if self._grenton_type == "RGB" or (self._grenton_type == "DIMMER" and self._grenton_id.split('->')[1].startswith("ZWA")):
                command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(0, 0)')"}
            elif self._grenton_type == "LED_R":
                command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(3, 0)')"}
            elif self._grenton_type == "LED_G":
                command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(4, 0)')"}
            elif self._grenton_type == "LED_B":
                command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(5, 0)')"}
            elif self._grenton_type == "LED_W":
                command = {"command": f"{self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:execute(12, 0)')"}
                
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    self._state = STATE_OFF
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to turn off the light: {ex}")

    async def async_update(self):
        try:
            command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(0)')"}
            if self._grenton_type == "RGB":
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command.update({"status_2": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(3)')"})
                else:
                    command.update({"status_2": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(6)')"})
            elif self._grenton_type == "LED_R":
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(0)')"}
                else:
                    command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(3)')"}
            elif self._grenton_type == "LED_G":
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(0)')"}
                else:
                    command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(4)')"}
            elif self._grenton_type == "LED_B":
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(0)')"}
                else:
                    command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(5)')"}
            elif self._grenton_type == "LED_W":
                if self._grenton_id.split('->')[1].startswith("ZWA"):
                    command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(0)')"}
                else:
                    command = {"status": f"return {self._grenton_id.split('->')[0]}:execute(0, '{self._grenton_id.split('->')[1]}:get(15)')"}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self._api_endpoint}", json=command) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self._state = STATE_OFF if data.get("status") == 0 else STATE_ON
                    if self._grenton_type == "RGB" or self._grenton_type == "DIMMER":
                        if self._grenton_type == "DIMMER" and self._grenton_id.split('->')[1].startswith("ZWA"):
                            self._brightness = data.get("status")
                        else:
                            self._brightness = data.get("status") * 255
                    elif self._grenton_type == "LED_R" or self._grenton_type == "LED_G" or self._grenton_type == "LED_B" or self._grenton_type == "LED_W":
                        self._brightness = data.get("status")
                    
                    if self._grenton_type == "RGB":
                        self._rgb_color = color_util.rgb_hex_to_rgb_list(data.get("status_2").strip("#"))
        except aiohttp.ClientError as ex:
            _LOGGER.error(f"Failed to update the light state: {ex}")
            self._state = None
