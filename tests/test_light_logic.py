import pytest
from unittest.mock import patch
from aioresponses import aioresponses
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from custom_components.grenton_objects.light import GrentonLight

@pytest.mark.asyncio
async def test_async_turn_on_dout():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test lIGHT"
    grenton_type = "DOUT"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
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
async def test_async_turn_on_dimmer():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DIM0000"
    object_name = "Test lIGHT"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness = 255
        assert obj.unique_id == "grenton_DIM0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'DIM0000:set(0, 1)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_zwave():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    object_name = "Test lIGHT"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness = 255
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ZWA0000:set(0, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_rgbw_r():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test lIGHT"
    grenton_type = "LED_R"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness = 255
        assert obj.unique_id == "grenton_LED0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:set(3, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_rgbw_g():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test lIGHT"
    grenton_type = "LED_G"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness = 255
        assert obj.unique_id == "grenton_LED0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:set(4, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_rgbw_b():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test lIGHT"
    grenton_type = "LED_B"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness = 255
        assert obj.unique_id == "grenton_LED0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:set(5, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_rgbw_w():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test lIGHT"
    grenton_type = "LED_W"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness = 255
        assert obj.unique_id == "grenton_LED0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:set(12, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_rgb():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test lIGHT"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on(rgb_color=[255, 255, 255])
        
        assert obj.is_on
        assert obj.rgb_color = [255, 255, 255]
        assert obj.unique_id == "grenton_LED0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:set(6, \"000000\")')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_rgb():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    object_name = "Test lIGHT"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on(rgb_color=[255, 255, 255])
        
        assert obj.is_on
        assert obj.rgb_color = [255, 255, 255]
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ZWA0000:set(3, \"000000\")')"}
        )
        
@pytest.mark.asyncio
async def test_async_turn_on_rgb_no_rgb_color():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->RGB0000"
    object_name = "Test lIGHT"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.rgb_color = [255, 255, 255]
        assert obj.unique_id == "grenton_RGB0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'RGB0000:set(0, 1)')"}
        )