import pytest
from custom_components.grenton_objects.light import GrentonLight
from homeassistant.const import STATE_ON, STATE_OFF

def create_obj(grenton_id="CLU220000000->DOU0000", grenton_type = "DOUT", response_data={"status": "ok"}, captured_command=None):
    obj = GrentonLight(
        api_endpoint="http://fake-api",
        grenton_id=grenton_id,
        object_name="Test obj",
        grenton_type = grenton_type,
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
async def test_async_turn_on_dout(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_type = "DOUT", response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_turn_on()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'DOU0000:set(0, 1)')"
    }
    assert obj.is_on
    assert obj._state == STATE_ON
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_DOU0000"

@pytest.mark.asyncio
async def test_async_turn_on_dimmer(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->DIM0000", grenton_type = "DIMMER", response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_turn_on()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'DIM0000:set(0, 1.0)')"
    }
    assert obj.is_on
    assert obj._state == STATE_ON
    assert obj.brightness == 255
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_DIM0000"