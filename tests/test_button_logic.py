import pytest
from custom_components.grenton_objects.button import GrentonScript

def create_sensor(grenton_id="my_script", status="ok", captured_command=None):
    sensor = GrentonScript(
        api_endpoint="http://fake-api",
        grenton_id=grenton_id,
        object_name="Test Script"
    )
    sensor._initialized = True

    class MockHass:
        def async_add_job(self, *args, **kwargs): pass
    sensor.hass = MockHass()
    sensor.async_write_ha_state = lambda: None

    class FakeResponse:
        async def json(self): return {"status": status}
        def raise_for_status(self): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass

    class FakeSession:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        def get(self, url, json):
            if captured_command is not None:
                captured_command["value"] = json
            return FakeResponse()

    return sensor, FakeSession

@pytest.mark.asyncio
async def test_async_script_local(monkeypatch):
    captured_command = {}
    sensor, FakeSession = create_sensor(status="ok", captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())

    assert captured_command["value"] == {
        "command": "my_script(nil)"
    }
    assert sensor.unique_id == "grenton_my_script"

@pytest.mark.asyncio
async def test_async_script_remote(monkeypatch):
    captured_command = {}
    sensor, FakeSession = create_sensor(grenton_id="CLU220000000->my_script_2", status="ok", captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'my_script_2(nil)')"
    }
    assert sensor.unique_id == "grenton_my_script_2"