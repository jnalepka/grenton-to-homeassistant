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
    object_name = "Test Light"
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
    object_name = "Test Light"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_DIM0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'DIM0000:set(0, 1.0)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_zwave():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    object_name = "Test Light"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ZWA0000:execute(0, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_rgbw_r():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "LED_R"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_LED0000_LED_R"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:execute(3, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_rgbw_g():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "LED_G"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_LED0000_LED_G"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:execute(4, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_rgbw_b():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "LED_B"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_LED0000_LED_B"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:execute(5, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_dimmer_rgbw_w():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "LED_W"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_LED0000_LED_W"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:execute(12, 255)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_rgb():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on(rgb_color=[255, 255, 255])
        
        assert obj.is_on
        assert obj.rgb_color == [255, 255, 255]
        assert obj.unique_id == "grenton_LED0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'LED0000:execute(6, \\\"#ffffff\\\")')"}
        )

@pytest.mark.asyncio
async def test_async_turn_on_rgb_zwave():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    object_name = "Test Light"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on(rgb_color=[0, 0, 0])
        
        assert obj.is_on
        assert obj.rgb_color == [0, 0, 0]
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ZWA0000:execute(3, \\\"#000000\\\")')"}
        )
        
@pytest.mark.asyncio
async def test_async_turn_on_rgb_no_rgb_color():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->RGB0000"
    object_name = "Test Light"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_on()
        
        assert obj.is_on
        assert obj.unique_id == "grenton_RGB0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'RGB0000:execute(0, 1.0)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_off_dout():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Light"
    grenton_type = "DOUT"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
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
async def test_async_turn_off_dimmer():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Light"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
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
async def test_async_turn_off_dimmer_zwave():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    object_name = "Test Light"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_off()
        
        assert not obj.is_on
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ZWA0000:execute(0, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_off_rgb():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->RGB0000"
    object_name = "Test Light"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_off()
        
        assert not obj.is_on
        assert obj.unique_id == "grenton_RGB0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'RGB0000:execute(0, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_off_rgb_led_r():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->RGB0000"
    object_name = "Test Light"
    grenton_type = "LED_R"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_off()
        
        assert not obj.is_on
        assert obj.unique_id == "grenton_RGB0000_LED_R"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'RGB0000:execute(3, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_off_rgb_led_g():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->RGB0000"
    object_name = "Test Light"
    grenton_type = "LED_G"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_off()
        
        assert not obj.is_on
        assert obj.unique_id == "grenton_RGB0000_LED_G"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'RGB0000:execute(4, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_off_rgb_led_b():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->RGB0000"
    object_name = "Test Light"
    grenton_type = "LED_B"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_off()
        
        assert not obj.is_on
        assert obj.unique_id == "grenton_RGB0000_LED_B"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'RGB0000:execute(5, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_off_rgb_led_w():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->RGB0000"
    object_name = "Test Light"
    grenton_type = "LED_W"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_turn_off()
        
        assert not obj.is_on
        assert obj.unique_id == "grenton_RGB0000_LED_W"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'RGB0000:execute(12, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_update_dout():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Light"
    grenton_type = "DOUT"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
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
async def test_async_update_dout_off():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DOU0000"
    object_name = "Test Light"
    grenton_type = "DOUT"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
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

@pytest.mark.asyncio
async def test_async_update_dimmer():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DIM0000"
    object_name = "Test Light"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 1})
        
        await obj.async_update()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_DIM0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'DIM0000:get(0)')"}
        )

@pytest.mark.asyncio
async def test_async_update_dimmer_off():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->DIM0000"
    object_name = "Test Light"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0})
        
        await obj.async_update()
        
        assert not obj.is_on
        assert obj.brightness == 0
        assert obj.unique_id == "grenton_DIM0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'DIM0000:get(0)')"}
        )

@pytest.mark.asyncio
async def test_async_update_dimmer_zwave():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    object_name = "Test Light"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 255})
        
        await obj.async_update()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'ZWA0000:get(0)')"}
        )

@pytest.mark.asyncio
async def test_async_update_dimmer_zwave_off():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    object_name = "Test Light"
    grenton_type = "DIMMER"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0})
        
        await obj.async_update()
        
        assert not obj.is_on
        assert obj.brightness == 0
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'ZWA0000:get(0)')"}
        )

@pytest.mark.asyncio
async def test_async_update_led_r():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "LED_R"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 255})
        
        await obj.async_update()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_LED0000_LED_R"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'LED0000:get(3)')"}
        )

@pytest.mark.asyncio
async def test_async_update_led_g_off():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "LED_G"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0})
        
        await obj.async_update()
        
        assert not obj.is_on
        assert obj.brightness == 0
        assert obj.unique_id == "grenton_LED0000_LED_G"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'LED0000:get(4)')"}
        )

@pytest.mark.asyncio
async def test_async_update_led_b_off():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "LED_B"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0})
        
        await obj.async_update()
        
        assert not obj.is_on
        assert obj.brightness == 0
        assert obj.unique_id == "grenton_LED0000_LED_B"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'LED0000:get(5)')"}
        )

@pytest.mark.asyncio
async def test_async_update_led_w():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "LED_W"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 255})
        
        await obj.async_update()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.unique_id == "grenton_LED0000_LED_W"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'LED0000:get(15)')"}
        )

@pytest.mark.asyncio
async def test_async_update_rgb():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 1, "status_2": "#000000"})
        
        await obj.async_update()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.rgb_color == [0, 0, 0]
        assert obj.unique_id == "grenton_LED0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'LED0000:get(0)')", "status_2": "return CLU220000000:execute(0, 'LED0000:get(6)')"}
        )

@pytest.mark.asyncio
async def test_async_update_rgb_off():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->LED0000"
    object_name = "Test Light"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0, "status_2": "#ffffff"})
        
        await obj.async_update()
        
        assert not obj.is_on
        assert obj.brightness == 0
        assert obj.rgb_color == [255, 255, 255]
        assert obj.unique_id == "grenton_LED0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'LED0000:get(0)')", "status_2": "return CLU220000000:execute(0, 'LED0000:get(6)')"}
        )

@pytest.mark.asyncio
async def test_async_update_rgb_zwave():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    object_name = "Test Light"
    grenton_type = "RGB"
    
    obj = GrentonLight(api_endpoint, grenton_id, grenton_type, object_name)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 1, "status_2": "#ffffff"})
        
        await obj.async_update()
        
        assert obj.is_on
        assert obj.brightness == 255
        assert obj.rgb_color == [255, 255, 255]
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'ZWA0000:get(0)')", "status_2": "return CLU220000000:execute(0, 'ZWA0000:get(3)')"}
        )
