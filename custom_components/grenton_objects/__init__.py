"""
==================================================
Author: Jan Nalepka
Script version: 3.1
Date: 01.10.2025
Repository: https://github.com/jnalepka/grenton-to-homeassistant
==================================================
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from homeassistant.exceptions import ServiceValidationError
import voluptuous as vol

SERVICE_SET_STATE_SCHEMA = vol.Schema({
    vol.Required("entity_id"): str,
    vol.Required("state"): vol.In([0, 1])
})

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    async def handle_set_state(call: ServiceCall) -> None:
        entity_id = call.data["entity_id"]
        state = call.data["state"]

        entity = hass.data.get(DOMAIN, {}).get("entities", {}).get(entity_id)
        if entity is None:
            raise ServiceValidationError(f"Encja {entity_id} nie została znaleziona")

        await entity.async_force_state(state)

    hass.services.async_register(
        DOMAIN,
        "set_state",
        handle_set_state,
        schema=SERVICE_SET_STATE_SCHEMA
    )
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
