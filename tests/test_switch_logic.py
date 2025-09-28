import pytest
from custom_components.grenton_objects.switch import GrentonSwitch
from homeassistant.const import STATE_ON, STATE_OFF

def create_obj(grenton_id="CLU220000000->DIN0000", response_data={"status": 1}, captured_command=None):
    obj = GrentonSwitch(
        api_endpoint="http://fake-api",
        grenton_id=grenton_id,
        object_name="Test Sensor",
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
async def test_async_turn_on(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->DOU0000", response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_turn_on()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'DOU0000:set(0, 1)')"
    }
    assert obj._state == STATE_ON
    assert obj.is_on is True
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_DOU0000"

@pytest.mark.asyncio
async def test_async_turn_off(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->DOU0000", response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_turn_off()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'DOU0000:set(0, 0)')"
    }
    assert obj._state == STATE_OFF
    assert not obj.is_on is True
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_DOU0000"

@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->DOU0000", response_data={"status": 1}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_update()

    assert captured_command["value"] == {
        "status": "return CLU220000000:execute(0, 'DOU0000:get(0)')"
    }
    assert obj._state == STATE_ON
    assert obj.is_on is True
    assert obj.unique_id == "grenton_DOU0000"

@pytest.mark.asyncio
async def test_async_update_off(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->DOU0000", response_data={"status": 0}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_update()

    assert captured_command["value"] == {
        "status": "return CLU220000000:execute(0, 'DOU0000:get(0)')"
    }
    assert obj._state == STATE_OFF
    assert not obj.is_on is True
    assert obj.unique_id == "grenton_DOU0000"