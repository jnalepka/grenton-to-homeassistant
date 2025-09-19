import pytest
from aioresponses import aioresponses
from custom_components.grenton_objects.switch import GrentonSwitch

@pytest.mark.asyncio
async def test_async_turn_on():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Switch"
    
    obj = GrentonSwitch(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    await hass.async_add_executor_job(lambda: None)
    await obj.async_added_to_hass()
    obj.hass = hass
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.unique_id == "grenton_DOU0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'DOU0000:set(0, 1)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_off():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Switch"
    
    obj = GrentonSwitch(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    await hass.async_add_executor_job(lambda: None)
    await obj.async_added_to_hass()
    obj.hass = hass
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_off()
        
        assert not obj.is_on
        assert obj.unique_id == "grenton_DOU0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'DOU0000:set(0, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_update():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Switch"
    
    obj = GrentonSwitch(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    await hass.async_add_executor_job(lambda: None)
    await obj.async_added_to_hass()
    obj.hass = hass
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 1})
        
        await obj.async_update()
        
        assert obj.is_on
        assert obj.unique_id == "grenton_DOU0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'DOU0000:get(0)')"}
        )

@pytest.mark.asyncio
async def test_async_update_off():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Switch"
    
    obj = GrentonSwitch(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    await hass.async_add_executor_job(lambda: None)
    await obj.async_added_to_hass()
    obj.hass = hass
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0}) 
        
        await obj.async_update()
        
        assert not obj.is_on
        assert obj.unique_id == "grenton_DOU0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'DOU0000:get(0)')"}
        )
