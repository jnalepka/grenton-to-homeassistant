import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON, STATE_OFF
from custom_components.grenton_to_homeassistant import GrentonSwitch  # Zaktualizuj ścieżkę importu

@pytest.fixture
def mock_aiohttp_post():
    """Fixture for mocking the aiohttp POST method."""
    with patch("aiohttp.ClientSession.post", new_callable=AsyncMock) as mock_post:
        yield mock_post

@pytest.fixture
def mock_aiohttp_get():
    """Fixture for mocking the aiohttp GET method."""
    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:
        yield mock_get

@pytest.fixture
def grenton_switch():
    """Fixture to create GrentonSwitch entity."""
    api_endpoint = "http://example.com/api"
    grenton_id = "part0->part1"
    object_name = "Test Switch"
    
    return GrentonSwitch(api_endpoint, grenton_id, object_name)

@pytest.mark.asyncio
async def test_last_command_on(grenton_switch, mock_aiohttp_post):
    """Test if the last command is set correctly for async_turn_on."""
    
    # Mocking the response from the API (successful command execution)
    mock_response = MagicMock()
    mock_response.raise_for_status = AsyncMock()
    mock_aiohttp_post.return_value = mock_response
    
    # Call async_turn_on
    await grenton_switch.async_turn_on()
    
    # Check if _tests_last_command is set correctly
    expected_command = {
        "command": "part0:execute(0, 'part1:set(0, 1)')"
    }
    assert grenton_switch._tests_last_command == expected_command

@pytest.mark.asyncio
async def test_last_command_off(grenton_switch, mock_aiohttp_post):
    """Test if the last command is set correctly for async_turn_off."""
    
    # Mocking the response from the API (successful command execution)
    mock_response = MagicMock()
    mock_response.raise_for_status = AsyncMock()
    mock_aiohttp_post.return_value = mock_response
    
    # Call async_turn_off
    await grenton_switch.async_turn_off()
    
    # Check if _tests_last_command is set correctly
    expected_command = {
        "command": "part0:execute(0, 'part1:set(0, 0)')"
    }
    assert grenton_switch._tests_last_command == expected_command

@pytest.mark.asyncio
async def test_last_command_update(grenton_switch, mock_aiohttp_get):
    """Test if the last command is set correctly for async_update."""
    
    # Mocking the response from the API (successful status retrieval)
    mock_response = MagicMock()
    mock_response.json = AsyncMock(return_value={"status": 1})
    mock_aiohttp_get.return_value = mock_response
    
    # Call async_update
    await grenton_switch.async_update()
    
    # Check if _tests_last_command is set correctly
    expected_command = {
        "status": "return part0:execute(0, 'part1:get(0)')"
    }
    assert grenton_switch._tests_last_command == expected_command

@pytest.mark.asyncio
async def test_state_on(grenton_switch, mock_aiohttp_get):
    """Test if the switch state is set to ON correctly."""
    
    # Mocking the response from the API (status 1 -> STATE_ON)
    mock_response = MagicMock()
    mock_response.json = AsyncMock(return_value={"status": 1})
    mock_aiohttp_get.return_value = mock_response
    
    # Call async_update to trigger state change
    await grenton_switch.async_update()
    
    # Check if state is set to STATE_ON
    assert grenton_switch.is_on is True

@pytest.mark.asyncio
async def test_state_off(grenton_switch, mock_aiohttp_get):
    """Test if the switch state is set to OFF correctly."""
    
    # Mocking the response from the API (status 0 -> STATE_OFF)
    mock_response = MagicMock()
    mock_response.json = AsyncMock(return_value={"status": 0})
    mock_aiohttp_get.return_value = mock_response
    
    # Call async_update to trigger state change
    await grenton_switch.async_update()
    
    # Check if state is set to STATE_OFF
    assert grenton_switch.is_on is False
