import pytest
from custom_components.grenton_objects.climate import GrentonClimate

def create_obj(grenton_id="CLU220000000->THE0000", status="ok", captured_command=None):
    obj = GrentonClimate(
        api_endpoint="http://fake-api",
        grenton_id=grenton_id,
        object_name="Test obj",
        auto_update=False,
        update_interval=5
    )
    obj._initialized = True

    class MockHass:
        def async_add_job(self, *args, **kwargs): pass
    obj.hass = MockHass()
    obj.async_write_ha_state = lambda: None

    class FakeResponse:
        async def json(self): return {"status": status}
        def raise_for_status(self): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass

    class FakeSession:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        def post(self, url, json):
            captured_command["value"] = json
            return FakeResponse()

    return obj, FakeSession

@pytest.mark.asyncio
async def test_async_set_temperature(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(status="ok", captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_set_temperature(temperature=20)

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'THE0000:set(8, 0)')", "command_2": f"CLU220000000:execute(0, 'THE0000:set(3, 20)')"
    }