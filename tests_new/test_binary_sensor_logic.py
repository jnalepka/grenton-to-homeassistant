import pytest
from custom_components.grenton_objects.binary_sensor import GrentonBinarySensor
from homeassistant.const import STATE_ON, STATE_OFF

@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    sensor = GrentonBinarySensor(
        api_endpoint="http://fake-api",
        grenton_id="CLU220000000->DIN0000",
        object_name="Test Sensor",
        auto_update=False,
        update_interval=5
    )
    sensor._initialized = True

    # Mock hass i metoda async_write_ha_state
    class MockHass:
        def async_add_job(self, *args, **kwargs): pass
    sensor.hass = MockHass()
    sensor.async_write_ha_state = lambda: None  # <-- kluczowa linia

    captured_command = {}

    class FakeResponse:
        async def json(self):
            return {"status": 1}
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
        "status": "return CLU220000000:execute(0, 'DIN0000:get(0)')"
    }
    assert sensor._state == STATE_ON
    assert sensor.is_on is False

@pytest.mark.asyncio
async def test_async_update_off(monkeypatch):
    sensor = GrentonBinarySensor(
        api_endpoint="http://fake-api",
        grenton_id="CLU220000000->DIN0000",
        object_name="Test Sensor",
        auto_update=False,
        update_interval=5
    )
    sensor._initialized = True

    # Mock hass i metoda async_write_ha_state
    class MockHass:
        def async_add_job(self, *args, **kwargs): pass
    sensor.hass = MockHass()
    sensor.async_write_ha_state = lambda: None  # <-- kluczowa linia

    captured_command = {}

    class FakeResponse:
        async def json(self):
            return {"status": 0}
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
        "status": "return CLU220000000:execute(0, 'DIN0000:get(0)')"
    }
    assert sensor._state == STATE_OFF
    assert sensor.is_on is True