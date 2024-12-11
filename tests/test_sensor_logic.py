import pytest
from unittest.mock import patch
from aioresponses import aioresponses
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from custom_components.grenton_objects.sensor import GrentonSensor

@pytest.mark.asyncio
async def test_async_update_palensenstemp():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->PAN0000"
    grenton_type = "DEFAULT_SENSOR"
    object_name = "Test Sensor"
    unit_of_measurement = "°C"
    device_class = "temperature"
    state_class = "measurement"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class)
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 22.4})
        
        await obj.async_update()
        assert obj.native_value == 22.4
        assert obj.native_unit_of_measurement == "°C"
        assert obj.device_class == "temperature"
        assert obj.state_class == "measurement"
        assert obj.unique_id == "grenton_PAN0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'PAN0000:get(0)')"}
        )
