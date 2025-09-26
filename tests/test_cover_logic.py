import pytest
from custom_components.grenton_objects.cover import GrentonCover
from homeassistant.const import (
    STATE_CLOSED,
    STATE_CLOSING,
    STATE_OPEN,
    STATE_OPENING
)

def create_obj(grenton_id="CLU220000000->ROL0000", response_data={"status": "ok"}, captured_command=None, reversed = False):
    obj = GrentonCover(
        api_endpoint="http://fake-api",
        grenton_id=grenton_id,
        reversed = reversed,
        object_name="Test obj",
        auto_update=False,
        update_interval=5
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
    assert obj.is_closed
    assert obj._state == STATE_CLOSED
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
    assert obj.is_closing
    assert obj._state == STATE_CLOSING
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_ROL0000"