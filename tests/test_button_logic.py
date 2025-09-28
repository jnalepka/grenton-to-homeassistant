import pytest
from custom_components.grenton_objects.button import GrentonScript

def create_obj(grenton_id="my_script", response_data={"status": "ok"}, captured_command=None):
    obj = GrentonScript(
        api_endpoint="http://fake-api",
        grenton_id=grenton_id,
        object_name="Test Script"
    )

    class MockHass:
        def async_add_job(self, *args, **kwargs): pass
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
async def test_async_script_local(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_press()

    assert captured_command["value"] == {
        "command": "my_script(nil)"
    }
    assert obj.unique_id == "grenton_my_script"

@pytest.mark.asyncio
async def test_async_script_remote(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->my_script_2", response_data={"status": "ok"}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_press()

    assert captured_command["value"] == {
        "command": "CLU220000000:execute(0, 'my_script_2(nil)')"
    }
    assert obj.unique_id == "grenton_my_script_2"