import pytest
from unittest.mock import AsyncMock, patch
from homeassistant.const import STATE_ON, STATE_OFF
from custom_components.grenton.switch import GrentonSwitch

# Mock configuration
MOCK_CONFIG = {
    "api_endpoint": "http://192.168.0.4/HAlistener",
    "grenton_id": "CLU220000000->DOU0000",
    "object_name": "Test Grenton Switch"
}

@pytest.fixture
def grenton_switch():
    return GrentonSwitch(
        MOCK_CONFIG["api_endpoint"],
        MOCK_CONFIG["grenton_id"],
        MOCK_CONFIG["object_name"]
    )

@pytest.mark.asyncio
async def test_turn_on(grenton_switch):
    with patch("aiohttp.ClientSession.post", new_callable=AsyncMock) as mock_post:
      
        await grenton_switch.async_turn_on()

        expected_command = {
            "command": f"CLU220000000:execute(0, 'DOU0000:set(0, 1)')"
        }

        mock_post.assert_called_once_with(
            MOCK_CONFIG["api_endpoint"], json=expected_command
        )
        assert grenton_switch._state == STATE_ON


@pytest.mark.asyncio
async def test_turn_off(grenton_switch):
    with patch("aiohttp.ClientSession.post", new_callable=AsyncMock) as mock_post:

        await grenton_switch.async_turn_off()

        expected_command = {
            "command": f"CLU220000000:execute(0, 'DOU0000:set(0, 0)')"
        }

        mock_post.assert_called_once_with(
            MOCK_CONFIG["api_endpoint"], json=expected_command
        )
        assert grenton_switch._state == STATE_OFF


@pytest.mark.asyncio
async def test_update(grenton_switch):
    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:

        mock_get.return_value.__aenter__.return_value.json = AsyncMock(
            return_value={"status": 1}
        )

        await grenton_switch.async_update()

        expected_command = {
            "status": f"return CLU220000000:execute(0, 'DOU0000:get(0)')"
        }

        mock_get.assert_called_once_with(MOCK_CONFIG["api_endpoint"], json=expected_command)
        assert grenton_switch._state == STATE_ON
