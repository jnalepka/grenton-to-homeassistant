"""
==================================================
Author: Jan Nalepka
Version: 2.0
Date: 2024-10-19
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    # This method is used for setting up the integration via YAML.
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Grenton objects from a config entry."""
    device = config_entry.data
    platform = device["device_type"]
    await hass.config_entries.async_forward_entry_setups(config_entry, {platform})

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    device_type = config_entry.data.get("device_type")
    unload_ok = await hass.config_entries.async_unload_platforms(config_entry, [device_type])
    
    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id, None)
    
    return unload_ok
