"""
==================================================
Author: Jan Nalepka
Version: 2.2.0
Date: 2024-12-01
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    device = config_entry.data
    platform = device["device_type"]
    if platform:
        await hass.config_entries.async_forward_entry_setups(config_entry, {platform})
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    device_type = config_entry.data.get("device_type")
    if device_type:
        unload_ok = await hass.config_entries.async_unload_platforms(config_entry, [device_type])
        return unload_ok
    return False
