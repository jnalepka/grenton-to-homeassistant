"""Grenton objects integration by Jan Nalepka."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "grenton_objects"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Grenton objects from yaml configuration."""
    # This method is used for setting up the integration via YAML.
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Grenton objects from a config entry."""
    device = config_entry.data

    platform = device["device_type"]
    await hass.config_entries.async_forward_entry_setups(config_entry, {platform})

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    
    # Uzyskaj typ urządzenia
    device_type = config_entry.data.get("device_type")

    # Unload the platform related to the config entry
    unload_ok = await hass.config_entries.async_unload_platforms(config_entry, [device_type])
    
    if unload_ok:
        # If the platforms are successfully unloaded, perform additional cleanup if necessary
        hass.data[DOMAIN].pop(config_entry.entry_id, None)
    
    return unload_ok
