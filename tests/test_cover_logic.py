import pytest
from custom_components.grenton_objects.cover import GrentonCover
from homeassistant.const import (
    STATE_CLOSED,
    STATE_CLOSING,
    STATE_OPEN,
    STATE_OPENING
)
from homeassistant.components.cover import CoverDeviceClass

def create_obj(grenton_id="CLU220000000->ROL0000", response_data={"status": "ok"}, captured_command=None, reversed=False):
    obj = GrentonCover(
        api_endpoint="http://fake-api",
        grenton_id=grenton_id,
        reversed = reversed,
        object_name="Test obj",
        auto_update=False,
        update_interval=5,
        device_class = CoverDeviceClass.BLIND.value
    )
    obj._initialized = True

    class MockLoop:
        def time(self):
            return 123.456

    class MockHass:
        def async_add_job(self, *args, **kwargs): pass
        loop = MockLoop()
    obj.hass = MockHass()
    obj.async_write_ha_state = lambda: None

    class FakeResponse:
        async def json(self): return response_data
        def raise_for_status(self): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass

    class FakeSession:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        def post(self, url, json):
            captured_command["value"] = json
            return FakeResponse()
        def get(self, url, json):
            if captured_command is not None:
                captured_command["value"] = json
            return FakeResponse()

    return obj, FakeSession

@pytest.mark.asyncio
async def test_async_open_cover(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_open_cover()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ROL0000:execute(0, 0)')"
    }
    assert obj.is_opening
    assert obj._state == STATE_OPENING
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ROL0000"

@pytest.mark.asyncio
async def test_async_close_cover(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_close_cover()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ROL0000:execute(1, 0)')"
    }
    assert obj.is_closing
    assert obj._state == STATE_CLOSING
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ROL0000"

@pytest.mark.asyncio
async def test_async_stop_cover(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_stop_cover()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ROL0000:execute(3, 0)')"
    }
    assert obj._state == STATE_OPEN
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ROL0000"

@pytest.mark.asyncio
async def test_async_set_cover_position(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_set_cover_position(position=100)

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ROL0000:execute(10, 100)')"
    }
    assert obj.is_opening
    assert obj._state == STATE_OPENING
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ROL0000"

@pytest.mark.asyncio
async def test_async_set_cover_position_reversed(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command, reversed = True)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_set_cover_position(position=100)

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ROL0000:execute(10, 0)')"
    }
    assert obj.is_opening
    assert obj._state == STATE_OPENING
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ROL0000"

@pytest.mark.asyncio
async def test_async_set_cover_position_zwave(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->ZWA0000", response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_set_cover_position(position=100)

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ZWA0000:execute(7, 100)')"
    }
    assert obj.is_opening
    assert obj._state == STATE_OPENING
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ZWA0000"

@pytest.mark.asyncio
async def test_async_set_cover_position_reversed_zwave(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->ZWA0000", response_data={"status": "ok"}, captured_command=captured_command, reversed = True)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_set_cover_position(position=100)

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ZWA0000:execute(7, 0)')"
    }
    assert obj.is_opening
    assert obj._state == STATE_OPENING
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ZWA0000"

@pytest.mark.asyncio
async def test_async_set_cover_tilt_position(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_set_cover_tilt_position(tilt_position=100)

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ROL0000:execute(9, 90)')"
    }
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ROL0000"

@pytest.mark.asyncio
async def test_async_open_cover_tilt(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_open_cover_tilt()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ROL0000:execute(9, 90)')"
    }
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ROL0000"

@pytest.mark.asyncio
async def test_async_close_cover_tilt(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_close_cover_tilt()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'ROL0000:execute(9, 0)')"
    }
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ROL0000"

@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": 1, "status_2": 50, "status_3": 90}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_update()

    assert captured_command["value"] == {
        "status": "return CLU220000000:execute(0, 'ROL0000:get(0)')", "status_2": "return CLU220000000:execute(0, 'ROL0000:get(7)')", "status_3": "return CLU220000000:execute(0, 'ROL0000:get(8)')"
    }
    assert obj.unique_id == "grenton_ROL0000"
    assert obj.is_opening
    assert obj.current_cover_position == 50
    assert obj.current_cover_tilt_position == 100

@pytest.mark.asyncio
async def test_async_update_zwave(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->ZWA0000", response_data={"status": 0, "status_2": 50, "status_3": 90}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_update()

    assert captured_command["value"] == {
        "status": "return CLU220000000:execute(0, 'ZWA0000:get(2)')", "status_2": "return CLU220000000:execute(0, 'ZWA0000:get(4)')", "status_3": "return CLU220000000:execute(0, 'ZWA0000:get(6)')"
    }
    assert obj.unique_id == "grenton_ZWA0000"
    assert not obj.is_closed
    assert obj.current_cover_position == 50
    assert obj.current_cover_tilt_position == 100

@pytest.mark.asyncio
async def test_async_update_reversed(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": 0, "status_2": 100, "status_3": 90}, captured_command=captured_command, reversed = True)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_update()

    assert captured_command["value"] == {
        "status": "return CLU220000000:execute(0, 'ROL0000:get(0)')", "status_2": "return CLU220000000:execute(0, 'ROL0000:get(7)')", "status_3": "return CLU220000000:execute(0, 'ROL0000:get(8)')"
    }
    assert obj.unique_id == "grenton_ROL0000"
    assert obj.is_closed
    assert obj.current_cover_position == 0
    assert obj.current_cover_tilt_position == 100

@pytest.mark.asyncio
async def test_async_update_zwave_reversed(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->ZWA0000", response_data={"status": 2, "status_2": 100, "status_3": 0}, captured_command=captured_command, reversed = True)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_update()

    assert captured_command["value"] == {
        "status": "return CLU220000000:execute(0, 'ZWA0000:get(2)')", "status_2": "return CLU220000000:execute(0, 'ZWA0000:get(4)')", "status_3": "return CLU220000000:execute(0, 'ZWA0000:get(6)')"
    }
    assert obj.unique_id == "grenton_ZWA0000"
    assert obj.is_closing
    assert obj.current_cover_position == 0
    assert obj.current_cover_tilt_position == 0