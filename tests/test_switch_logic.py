import pytest
from unittest.mock import AsyncMock, patch
from homeassistant.const import STATE_ON, STATE_OFF
from custom_components.grenton_objects.switch import GrentonSwitch

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
        # Konfiguracja mocka, aby działał poprawnie w async with
        mock_response = AsyncMock()
        mock_response.__aenter__.return_value.status = 200
        mock_post.return_value = mock_response

        await grenton_switch.async_turn_on()

        mock_post.assert_called_once_with(
            f"{grenton_switch._api_endpoint}",
            json={"command": "CLU220000000:execute(0, 'DOU0000:set(0, 1)')"},
        )


@pytest.mark.asyncio
async def test_turn_off(grenton_switch):
    with patch("aiohttp.ClientSession.post", new_callable=AsyncMock) as mock_post:
        mock_response = AsyncMock()
        mock_response.__aenter__.return_value.status = 200
        mock_post.return_value = mock_response

        await grenton_switch.async_turn_off()

        mock_post.assert_called_once_with(
            f"{grenton_switch._api_endpoint}",
            json={"command": "CLU220000000:execute(0, 'DOU0000:set(0, 0)')"},
        )


@pytest.mark.asyncio
async def test_update(grenton_switch):
    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.__aenter__.return_value.json = AsyncMock(
            return_value={"status": 1}
        )
        mock_get.return_value = mock_response

        await grenton_switch.async_update()

        mock_get.assert_called_once_with(
            f"{grenton_switch._api_endpoint}",
            json={"status": "return CLU220000000:execute(0, 'DOU0000:get(0)')"},
        )
