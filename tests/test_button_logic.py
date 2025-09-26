import pytest
from custom_components.grenton_objects.button import GrentonScript
from homeassistant.const import STATE_ON, STATE_OFF

@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    sensor = GrentonScript(
        api_endpoint="http://fake-api",
        grenton_id="my_script",
        object_name="Test Script",
        auto_update=False,
        update_interval=5
    )
    sensor._initialized = True

    class MockHass:
        def async_add_job(self, *args, **kwargs): pass
    sensor.hass = MockHass()
    sensor.async_write_ha_state = lambda: None

    captured_command = {}

    class FakeResponse:
        async def json(self):
            return {"status": "ok"}
        def raise_for_status(self):
            pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass

    class FakeSession:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        def get(self, url, json):
            captured_command["value"] = json
            return FakeResponse()

    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())

    await sensor.async_update()

    assert captured_command["value"] == {
        "command": "my_script(nil)"
    }