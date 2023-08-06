from zainpay.utils.api_client.client import APIClient
from zainpay.utils.constants import DEVELOPMENT_URL, MODES, PRODUCTION_URL


class APIClientFactory(APIClient):
    def __init__(self, mode: MODES = MODES.DEVELOPMENT) -> None:
        base_url: str

        match (mode):
            case MODES.DEVELOPMENT:
                base_url = DEVELOPMENT_URL
            case MODES.PRODUCTION:
                base_url = PRODUCTION_URL
            case _:
                raise NotImplementedError()

        super().__init__(base_url)
