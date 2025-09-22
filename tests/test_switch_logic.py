import pytest
from aioresponses import aioresponses
from custom_components.grenton_objects.switch import GrentonSwitch
from homeassistant.core import HomeAssistant

@pytest.mark.asyncio
async def test_async_turn_on():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Switch"
    
    obj = GrentonSwitch(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
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
    if obj._unsub_interval:
        obj._unsub_interval()

@pytest.mark.asyncio
async def test_async_turn_off():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Switch"
    
    obj = GrentonSwitch(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
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
    if obj._unsub_interval:
        obj._unsub_interval()

@pytest.mark.asyncio
async def test_async_update():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Switch"
    
    obj = GrentonSwitch(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
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
    if obj._unsub_interval:
        obj._unsub_interval()

@pytest.mark.asyncio
async def test_async_update_off():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Switch"
    
    obj = GrentonSwitch(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
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
    if obj._unsub_interval:
        obj._unsub_interval()
