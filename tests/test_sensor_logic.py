import pytest
from aioresponses import aioresponses
from custom_components.grenton_objects.sensor import GrentonSensor
from homeassistant.core import HomeAssistant

@pytest.mark.asyncio
async def test_async_update_palensenstemp():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->PAN0000"
    grenton_type = "DEFAULT_SENSOR"
    object_name = "Test Sensor"
    unit_of_measurement = "°C"
    device_class = "temperature"
    state_class = "measurement"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
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

@pytest.mark.asyncio
async def test_async_update_gate_feature():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "my_feature_123"
    grenton_type = "DEFAULT_SENSOR"
    object_name = "Test Sensor"
    unit_of_measurement = "km/h"
    device_class = "wind_speed"
    state_class = "measurement"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 50.5})
        
        await obj.async_update()
        assert obj.native_value == 50.5
        assert obj.native_unit_of_measurement == "km/h"
        assert obj.device_class == "wind_speed"
        assert obj.state_class == "measurement"
        assert obj.unique_id == "grenton_my_feature_123"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return getVar(\"my_feature_123\")"}
        )

@pytest.mark.asyncio
async def test_async_update_clu_feature():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->my_feature_123"
    grenton_type = "DEFAULT_SENSOR"
    object_name = "Test Sensor"
    unit_of_measurement = "km/h"
    device_class = "wind_speed"
    state_class = "measurement"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 50.5})
        
        await obj.async_update()
        assert obj.native_value == 50.5
        assert obj.native_unit_of_measurement == "km/h"
        assert obj.device_class == "wind_speed"
        assert obj.state_class == "measurement"
        assert obj.unique_id == "grenton_my_feature_123"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'getVar(\"my_feature_123\")')"}
        )

@pytest.mark.asyncio
async def test_async_update_clu_feature_contain_obj_id():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->when_DOU1234_light_up"
    grenton_type = "DEFAULT_SENSOR"
    object_name = "Test Sensor"
    unit_of_measurement = "%"
    device_class = "humidity"
    state_class = "measurement"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 100})
        
        await obj.async_update()
        assert obj.native_value == 100
        assert obj.native_unit_of_measurement == "%"
        assert obj.device_class == "humidity"
        assert obj.state_class == "measurement"
        assert obj.unique_id == "grenton_when_DOU1234_light_up"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'getVar(\"when_DOU1234_light_up\")')"}
        )

@pytest.mark.asyncio
async def test_async_update_modbus():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->MOD0000"
    grenton_type = "MODBUS"
    object_name = "Test Sensor"
    unit_of_measurement = "kWh"
    device_class = "energy"
    state_class = "total"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 192349.12})
        
        await obj.async_update()
        assert obj.native_value == 192349.12
        assert obj.native_unit_of_measurement == "kWh"
        assert obj.device_class == "energy"
        assert obj.state_class == "total"
        assert obj.unique_id == "grenton_MOD0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'MOD0000:get(14)')"}
        )

@pytest.mark.asyncio
async def test_async_update_modbus_value():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->MOD0000"
    grenton_type = "MODBUS_VALUE"
    object_name = "Test Sensor"
    unit_of_measurement = "kWh"
    device_class = "energy"
    state_class = "total_increasing"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0.01})
        
        await obj.async_update()
        assert obj.native_value == 0.01
        assert obj.native_unit_of_measurement == "kWh"
        assert obj.device_class == "energy"
        assert obj.state_class == "total_increasing"
        assert obj.unique_id == "grenton_MOD0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'MOD0000:get(20)')"}
        )

@pytest.mark.asyncio
async def test_async_update_modbus_rtu():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->MOD0000"
    grenton_type = "MODBUS_RTU"
    object_name = "Test Sensor"
    unit_of_measurement = "W"
    device_class = "power"
    state_class = "measurement"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 0.1})
        
        await obj.async_update()
        assert obj.native_value == 0.1
        assert obj.native_unit_of_measurement == "W"
        assert obj.device_class == "power"
        assert obj.state_class == "measurement"
        assert obj.unique_id == "grenton_MOD0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'MOD0000:get(22)')"}
        )

@pytest.mark.asyncio
async def test_async_update_modbus_client():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->MOD0000"
    grenton_type = "MODBUS_CLIENT"
    object_name = "Test Sensor"
    unit_of_measurement = None
    device_class = "ph"
    state_class = "measurement"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 192349.12})
        
        await obj.async_update()
        assert obj.native_value == 192349.12
        assert obj.native_unit_of_measurement == None
        assert obj.device_class == "ph"
        assert obj.state_class == "measurement"
        assert obj.unique_id == "grenton_MOD0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'MOD0000:get(19)')"}
        )

@pytest.mark.asyncio
async def test_async_update_modbus_server():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->MOD0000"
    grenton_type = "MODBUS_SERVER"
    object_name = "Test Sensor"
    unit_of_measurement = "L"
    device_class = "water"
    state_class = "measurement"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 60})
        
        await obj.async_update()
        assert obj.native_value == 60
        assert obj.native_unit_of_measurement == "L"
        assert obj.device_class == "water"
        assert obj.state_class == "measurement"
        assert obj.unique_id == "grenton_MOD0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'MOD0000:get(10)')"}
        )

@pytest.mark.asyncio
async def test_async_update_modbus_slave_rtu():
    hass = HomeAssistant(config_dir="/tmp")
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->MOD0000"
    grenton_type = "MODBUS_SLAVE_RTU"
    object_name = "Test Sensor"
    unit_of_measurement = "ppb"
    device_class = "volatile_organic_compounds_parts"
    state_class = "measurement"
    
    obj = GrentonSensor(api_endpoint, grenton_id, grenton_type, object_name, unit_of_measurement, device_class, state_class, True, 5)
    obj._initialized = True
    obj.hass = hass
    await obj.async_added_to_hass()
    
    with aioresponses() as m:
        m.get(api_endpoint, status=200, payload={"status": 401.1})
        
        await obj.async_update()
        assert obj.native_value == 401.1
        assert obj.native_unit_of_measurement == "ppb"
        assert obj.device_class == "volatile_organic_compounds_parts"
        assert obj.state_class == "measurement"
        assert obj.unique_id == "grenton_MOD0000"
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return CLU220000000:execute(0, 'MOD0000:get(10)')"}
        )
