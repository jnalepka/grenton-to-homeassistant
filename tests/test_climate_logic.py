import pytest
from aioresponses import aioresponses
from custom_components.grenton_objects.climate import GrentonClimate
from homeassistant.components.climate import HVACMode

@pytest.mark.asyncio
async def test_async_set_temperature():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->THE0000"
    object_name = "Test Thermostat"
    
    obj = GrentonClimate(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    await hass.async_add_executor_job(lambda: None)
    await obj.async_added_to_hass()
    obj.hass = hass
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_set_temperature()
        
        assert obj.unique_id == "grenton_THE0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'THE0000:set(8, 0)')", "command_2": f"CLU220000000:execute(0, 'THE0000:set(3, 20)')"}
        )

@pytest.mark.asyncio
async def test_async_set_hvac_mode_heat():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->THE0000"
    object_name = "Test Thermostat"
    
    obj = GrentonClimate(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    await hass.async_add_executor_job(lambda: None)
    await obj.async_added_to_hass()
    obj.hass = hass
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_set_hvac_mode(HVACMode.HEAT)
        
        assert obj.unique_id == "grenton_THE0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'THE0000:execute(0, 0)')", "command_2": f"CLU220000000:execute(0, 'THE0000:set(7, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_set_hvac_mode_cool():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->THE0000"
    object_name = "Test Thermostat"
    
    obj = GrentonClimate(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    await hass.async_add_executor_job(lambda: None)
    await obj.async_added_to_hass()
    obj.hass = hass
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_set_hvac_mode(HVACMode.COOL)
        
        assert obj.unique_id == "grenton_THE0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'THE0000:execute(0, 0)')", "command_2": f"CLU220000000:execute(0, 'THE0000:set(7, 1)')"}
        )

@pytest.mark.asyncio
async def test_async_update():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->THE0000"
    object_name = "Test Thermostat"
    
    obj = GrentonClimate(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    await hass.async_add_executor_job(lambda: None)
    await obj.async_added_to_hass()
    obj.hass = hass
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 1, "status_2": 1, "status_3": 22, "status_4": 19})
        
        await obj.async_update()
        
        assert obj.unique_id == "grenton_THE0000"
        assert obj.hvac_mode == HVACMode.COOL
        assert obj.target_temperature == 22
        assert obj.current_temperature == 19
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'THE0000:get(6)')", "status_2": "return CLU220000000:execute(0, 'THE0000:get(7)')", "status_3": "return CLU220000000:execute(0, 'THE0000:get(12)')", "status_4": "return CLU220000000:execute(0, 'THE0000:get(14)')"}
        )
