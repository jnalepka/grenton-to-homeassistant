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
    
    devices = config_entry.data.get("devices", [])
    platforms = {device["device_type"] for device in devices}

    # Forward setup to the correct platforms
    await hass.config_entries.async_forward_entry_setups(config_entry, platforms)

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    
    # Unload the platforms related to the config entry
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, ["light", "switch", "climate", "cover", "sensor", "binary_sensor"]
    )
    
    if unload_ok:
        # If the platforms are successfully unloaded, perform additional cleanup if necessary
        hass.data[DOMAIN].pop(config_entry.entry_id, None)
    
    return unload_ok
