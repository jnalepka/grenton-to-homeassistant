import pytest
from custom_components.grenton_objects.climate import GrentonClimate
from homeassistant.components.climate import HVACMode

def create_obj(grenton_id="CLU220000000->THE0000", response_data={"status": "ok"}, captured_command=None):
    obj = GrentonClimate(
        api_endpoint="http://fake-api",
        grenton_id=grenton_id,
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
async def test_async_set_temperature(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_set_temperature(temperature=20)

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'THE0000:set(8, 0)')", "command_2": f"CLU220000000:execute(0, 'THE0000:set(3, 20)')"
    }
    assert obj._target_temperature == 20
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_THE0000"

@pytest.mark.asyncio
async def test_async_set_hvac_mode_heat(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_set_hvac_mode(HVACMode.HEAT)

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'THE0000:execute(0, 0)')", "command_2": f"CLU220000000:execute(0, 'THE0000:set(7, 0)')"
    }
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_THE0000"
    assert obj._hvac_mode == HVACMode.HEAT

@pytest.mark.asyncio
async def test_async_set_hvac_mode_cool(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_set_hvac_mode(HVACMode.COOL)

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'THE0000:execute(0, 0)')", "command_2": f"CLU220000000:execute(0, 'THE0000:set(7, 1)')"
    }
    assert obj._last_command_time == 123.456
    assert obj.unique_id == "grenton_THE0000"
    assert obj._hvac_mode == HVACMode.COOL

@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": 1, "status_2": 1, "status_3": 22, "status_4": 19}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_update()

    assert captured_command["value"] == {
        "status": "return CLU220000000:execute(0, 'THE0000:get(6)')", "status_2": "return CLU220000000:execute(0, 'THE0000:get(7)')", "status_3": "return CLU220000000:execute(0, 'THE0000:get(12)')", "status_4": "return CLU220000000:execute(0, 'THE0000:get(14)')"
    }
    assert obj._last_command_time == None
    assert obj.unique_id == "grenton_THE0000"
    assert obj._hvac_mode == HVACMode.COOL
    assert obj.target_temperature == 22
    assert obj.current_temperature == 19