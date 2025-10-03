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
from homeassistant.helpers import config_validation as cv

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

SERVICE_SET_STATE_SCHEMA = vol.Schema({
    vol.Required("entity_id"): str,
    vol.Required("state"): vol.In([0, 1])
})

SERVICE_SET_BRIGHTNESS_SCHEMA = vol.Schema({
    vol.Required("entity_id"): str,
    vol.Required("brightness"): vol.All(
        vol.Coerce(float),
        vol.Range(min=0.0, max=255.0)
    )
})

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    async def handle_set_state(call: ServiceCall) -> None:
        entity_id = call.data["entity_id"]
        state = call.data["state"]

        entity = hass.data.get(DOMAIN, {}).get("entities", {}).get(entity_id)
        if entity is None:
            raise ServiceValidationError(f"Encja {entity_id} nie została znaleziona")

        try:
            await entity.async_force_state(state)
        except Exception as err:
            raise ServiceValidationError(
                f"Nie udało się ustawić stanu dla encji {entity_id}: {err}"
            ) from err
        
    async def handle_set_brightness(call: ServiceCall) -> None:
        entity_id = call.data["entity_id"]
        brightness = call.data["brightness"]

        entity = hass.data.get(DOMAIN, {}).get("entities", {}).get(entity_id)
        if entity is None:
            raise ServiceValidationError(f"Encja {entity_id} nie została znaleziona")

        try:
            await entity.async_force_brightness(brightness)
        except Exception as err:
            raise ServiceValidationError(
                f"Nie udało się ustawić jasności dla encji {entity_id}: {err}"
            ) from err

    hass.services.async_register(
        DOMAIN,
        "set_state",
        handle_set_state,
        schema=SERVICE_SET_STATE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN,
        "set_brightness",
        handle_set_brightness,
        schema=SERVICE_SET_BRIGHTNESS_SCHEMA
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
