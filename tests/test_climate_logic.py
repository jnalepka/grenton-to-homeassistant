import pytest
from unittest.mock import patch
from aioresponses import aioresponses
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from custom_components.grenton_objects.climate import GrentonClimate

@pytest.mark.asyncio
async def test_async_turn_on():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->THE0000"
    object_name = "Test Thermostat"
    
    obj = GrentonClimate(api_endpoint, grenton_id, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_set_temperature()
        
        assert obj.unique_id == "grenton_THE0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'THE0000:set(8, 0)')", "command_2": f"CLU220000000:execute(0, 'THE0000:set(3, 20)')"}
        )
