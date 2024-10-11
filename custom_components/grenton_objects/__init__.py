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

    for device in devices:
        if device["device_type"] == "light":
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(config_entry, "light")
            )
        elif device["device_type"] == "switch":
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(config_entry, "switch")
            )
        elif device["device_type"] == "climate":
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(config_entry, "climate")
            )
        elif device["device_type"] == "cover":
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(config_entry, "cover")
            )
        elif device["device_type"] == "sensor":
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
            )
        elif device["device_type"] == "binary_sensor":
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(config_entry, "binary_sensor")
            )

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, ["light", "switch", "climate", "cover", "sensor", "binary_sensor"]
    )
    return unload_ok
