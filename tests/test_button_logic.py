import pytest
from aioresponses import aioresponses
from custom_components.grenton_objects.button import GrentonScript

@pytest.mark.asyncio
async def test_async_script_local():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "my_script"
    object_name = "Test Script"
    
    obj = GrentonScript(api_endpoint, grenton_id, object_name)
    obj._initialized = True
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_press()
        
        assert obj.unique_id == "grenton_my_script"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "my_script(nil)"}
        )

@pytest.mark.asyncio
async def test_async_script_remote():
    api_endpoint = "http://192.168.0.4/HAlistener"
    grenton_id = "CLU220000000->my_script_2"
    object_name = "Test Script"
    
    obj = GrentonScript(api_endpoint, grenton_id, object_name)
    obj._initialized = True
    
    with aioresponses() as m:
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await obj.async_press()
        
        assert obj.unique_id == "grenton_my_script_2"
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "CLU220000000:execute(0, 'my_script_2(nil)')"}
        )
