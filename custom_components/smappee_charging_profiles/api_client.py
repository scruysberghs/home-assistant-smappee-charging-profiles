import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

class SmappeeApiClient:
    def __init__(self, oauth_client):
        self.oauth_client = oauth_client
        self.base_url = "https://app1pub.smappee.net/dev/v3"

    async def set_charging_mode(self, serial, mode, limit):
        """Set the charging mode for the given serial number and connector."""
        # Ensure token is refreshed if needed
        if not self.oauth_client.access_token:
            await self.oauth_client.authenticate()

        url = f"{self.base_url}/chargingstations/{serial}/connectors/1/mode"
        headers = {
            "Authorization": f"Bearer {self.oauth_client.access_token}",
            "Content-Type": "application/json",
        }
        # Create the base payload with the mode
        payload = {
            "mode": mode
        }

        # Add the limit only if the mode is NORMAL
        if mode == "NORMAL":
            payload["limit"] = {
                "unit": "AMPERE",
                "value": limit
            }

        _LOGGER.debug(f"Sending request to {url} with payload {payload}")

        # Make the API request to set the charging mode
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.put(url, json=payload, headers=headers)
                if response.status != 200:
                    error_message = await response.text()
                    _LOGGER.error(f"Failed to set charging mode: {error_message}")
                    raise Exception(f"Error setting charging mode: {error_message}")
                _LOGGER.debug("Successfully set charging mode")
        except Exception as e:
            _LOGGER.error(f"Exception occurred while setting charging mode: {str(e)}")
            raise