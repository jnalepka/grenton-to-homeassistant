import pytest
from aioresponses import aioresponses
from custom_components.grenton_objects.cover import GrentonCover

@pytest.mark.asyncio
async def test_async_open_cover():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_open_cover()
        assert obj.is_opening
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ROL0000:execute(0, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_close_cover():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_close_cover()
        assert obj.is_closing
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ROL0000:execute(1, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_stop_cover():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_stop_cover()
        assert not obj.is_closed
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ROL0000:execute(3, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_set_cover_position():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_set_cover_position()
        assert obj.is_opening
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ROL0000:execute(10, 100)')"}
        )
      
@pytest.mark.asyncio
async def test_async_set_cover_position_reversed():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = True
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_set_cover_position()
        assert obj.is_opening
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ROL0000:execute(10, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_set_cover_position_zwave():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_set_cover_position()
        assert obj.is_opening
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ZWA0000:execute(7, 100)')"}
        )

@pytest.mark.asyncio
async def test_async_set_cover_position_reversed_zwave():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    reversed = True
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_set_cover_position()
        assert obj.is_opening
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ZWA0000:execute(7, 0)')"}
        )


@pytest.mark.asyncio
async def test_async_set_cover_tilt_position():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_set_cover_tilt_position()
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ROL0000:execute(9, 90)')"}
        )

@pytest.mark.asyncio
async def test_async_open_cover_tilt():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_open_cover_tilt()
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ROL0000:execute(9, 90)')"}
        )

@pytest.mark.asyncio
async def test_async_close_cover_tilt():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_close_cover_tilt()
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'ROL0000:execute(9, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_update():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 1, "status_2": 50, "status_3": 90})
        
        await obj.async_update()
        assert obj.is_opening
        assert obj.current_cover_position == 50
        assert obj.current_cover_tilt_position == 100
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'ROL0000:get(0)')", "status_2": "return CLU220000000:execute(0, 'ROL0000:get(7)')", "status_3": "return CLU220000000:execute(0, 'ROL0000:get(8)')"}
        )

@pytest.mark.asyncio
async def test_async_update_zwave():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    reversed = False
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0, "status_2": 50, "status_3": 90})
        
        await obj.async_update()
        assert not obj.is_closed
        assert obj.current_cover_position == 50
        assert obj.current_cover_tilt_position == 100
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'ZWA0000:get(2)')", "status_2": "return CLU220000000:execute(0, 'ZWA0000:get(4)')", "status_3": "return CLU220000000:execute(0, 'ZWA0000:get(6)')"}
        )

@pytest.mark.asyncio
async def test_async_update_reversed():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ROL0000"
    reversed = True
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0, "status_2": 100, "status_3": 90})
        
        await obj.async_update()
        assert obj.is_closed
        assert obj.current_cover_position == 0
        assert obj.current_cover_tilt_position == 100
        assert obj.unique_id == "grenton_ROL0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'ROL0000:get(0)')", "status_2": "return CLU220000000:execute(0, 'ROL0000:get(7)')", "status_3": "return CLU220000000:execute(0, 'ROL0000:get(8)')"}
        )

@pytest.mark.asyncio
async def test_async_update_zwave_reversed():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->ZWA0000"
    reversed = True
    object_name = "Test Cover"
    
    obj = GrentonCover(api_endpoint, grenton_id, reversed, object_name, True, 5)
    obj._initialized = True
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 2, "status_2": 100, "status_3": 0})
        
        await obj.async_update()
        assert obj.is_closing
        assert obj.current_cover_position == 0
        assert obj.current_cover_tilt_position == 0
        assert obj.unique_id == "grenton_ZWA0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'ZWA0000:get(2)')", "status_2": "return CLU220000000:execute(0, 'ZWA0000:get(4)')", "status_3": "return CLU220000000:execute(0, 'ZWA0000:get(6)')"}
        )
