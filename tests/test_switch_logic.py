import pytest
from unittest.mock import patch
from aioresponses import aioresponses
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from homeassistant.const import STATE_ON, STATE_OFF
from custom_components.grenton_objects.switch import GrentonSwitch

@pytest.mark.asyncio
async def test_async_turn_on():
    # Przygotowanie testowego obiektu switch
    api_endpoint = "http://localhost/api"
    grenton_id = "device1->switch1"
    object_name = "Test Switch"
    
    switch = GrentonSwitch(api_endpoint, grenton_id, object_name)
    
    with aioresponses() as m:
        # Symulujemy odpowiedź na zapytanie POST
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await switch.async_turn_on()
        
        # Sprawdź, czy stan switcha został ustawiony na "ON"
        assert switch.is_on
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "device1:execute(0, 'switch1:set(0, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_turn_off():
    api_endpoint = "http://localhost/api"
    grenton_id = "device1->switch1"
    object_name = "Test Switch"
    
    switch = GrentonSwitch(api_endpoint, grenton_id, object_name)
    
    with aioresponses() as m:
        # Symulujemy odpowiedź na zapytanie POST
        m.post(api_endpoint, status=200, payload={"status": "ok"})
        
        await switch.async_turn_off()
        
        # Sprawdź, czy stan switcha został ustawiony na "OFF"
        assert not switch.is_on
        m.assert_called_once_with(
            api_endpoint,
            method='POST',
            json={"command": "device1:execute(0, 'switch1:set(0, 0)')"}
        )

@pytest.mark.asyncio
async def test_async_update():
    api_endpoint = "http://localhost/api"
    grenton_id = "device1->switch1"
    object_name = "Test Switch"
    
    switch = GrentonSwitch(api_endpoint, grenton_id, object_name)
    
    with aioresponses() as m:
        # Symulujemy odpowiedź na zapytanie GET
        m.get(api_endpoint, status=200, payload={"status": 1})  # Switch is ON
        
        await switch.async_update()
        
        # Sprawdź, czy stan switcha został zaktualizowany na "ON"
        assert switch.is_on
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return device1:execute(0, 'switch1:get(0)')"}
        )

@pytest.mark.asyncio
async def test_async_update_off():
    api_endpoint = "http://localhost/api"
    grenton_id = "device1->switch1"
    object_name = "Test Switch"
    
    switch = GrentonSwitch(api_endpoint, grenton_id, object_name)
    
    with aioresponses() as m:
        # Symulujemy odpowiedź na zapytanie GET
        m.get(api_endpoint, status=200, payload={"status": 0})  # Switch is OFF
        
        await switch.async_update()
        
        # Sprawdź, czy stan switcha został zaktualizowany na "OFF"
        assert not switch.is_on
        m.assert_called_once_with(
            api_endpoint,
            method='GET',
            json={"status": "return device1:execute(0, 'switch1:get(0)')"}
        )
