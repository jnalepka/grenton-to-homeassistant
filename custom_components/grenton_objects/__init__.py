"""Grenton objects integration by Jan Nalepka."""

async def async_setup_entry(hass, config_entry):
    """Set up Grenton from a config entry."""
    
    devices = config_entry.data["devices"]

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
