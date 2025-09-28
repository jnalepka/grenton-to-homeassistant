import pytest
from custom_components.grenton_objects.binary_sensor import GrentonSensor

def create_obj(grenton_id="CLU220000000->DIN0000", grenton_type = "DEFAULT_SENSOR", unit_of_measurement = "°C", device_class = "temperature", state_class = "measurement", response_data={"status": 1}, captured_command=None):
    obj = GrentonSensor(
        api_endpoint="http://fake-api",
        grenton_id=grenton_id,
        grenton_type = grenton_type,
        object_name="Test Sensor",
        unit_of_measurement = unit_of_measurement,
        device_class = device_class,
        state_class = state_class,
        auto_update=False,
        update_interval=5
    )
    obj._initialized = True

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
async def test_async_update_panelsenstemp(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->DIN0000", grenton_type = "DEFAULT_SENSOR", unit_of_measurement = "°C", device_class = "temperature", state_class = "measurement", response_data={"status": 22.4}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_update()

    assert captured_command["value"] == {
        "status": "return CLU220000000:execute(0, 'PAN0000:get(0)')"
    }
    assert obj.native_value == 22.4
    assert obj.native_unit_of_measurement == "°C"
    assert obj.device_class == "temperature"
    assert obj.state_class == "measurement"
    assert obj.unique_id == "grenton_PAN0000"

@pytest.mark.asyncio
async def test_async_update_gate_feature(monkeypatch):
    captured_command = {}
    obj, FakeSession = create_obj(grenton_id="CLU220000000->DIN0000", grenton_type = "DEFAULT_SENSOR", unit_of_measurement = "km/h", device_class = "wind_speed", state_class = "measurement", response_data={"status": 50.5}, captured_command=captured_command)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: FakeSession())
    await obj.async_update()

    assert captured_command["value"] == {
        "status": "return getVar(\"my_feature_123\")"
    }
    assert obj.native_value == 50.5
    assert obj.native_unit_of_measurement == "km/h"
    assert obj.device_class == "wind_speed"
    assert obj.state_class == "measurement"
    assert obj.unique_id == "grenton_my_feature_123"