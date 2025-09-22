import pytest
from aioresponses import aioresponses
from custom_components.grenton_objects.binary_sensor import GrentonBinarySensor
from homeassistant.core import HomeAssistant

@pytest.mark.asyncio
async def test_async_update():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DIN0000"
    object_name = "Test Binary Sensor"
    
    obj = GrentonBinarySensor(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 1})
        
        await obj.async_update()
        
        assert obj.is_on
        assert obj.unique_id == "grenton_DIN0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'DIN0000:get(0)')"}
        )
    if obj._unsub_interval:
        obj._unsub_interval()

@pytest.mark.asyncio
async def test_async_update_off():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DIN0000"
    object_name = "Test Binary Sensor"
    
    obj = GrentonBinarySensor(api_endpoint, grenton_id, object_name, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0}) 
        
        await obj.async_update()
        
        assert not obj.is_on
        assert obj.unique_id == "grenton_DIN0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'DIN0000:get(0)')"}
        )
    if obj._unsub_interval:
        obj._unsub_interval()
