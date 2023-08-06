import pydantic

from zainpay.utils.api_client.client import APIClient
from zainpay.utils.api_client.factory import APIClientFactory
from zainpay.utils.constants import MODES, REQUEST_METHODS


class ZainBox:

    """
    A zainbox is a virtual bucket that allows a merchant to create unlimited multiple virtual accounts.
    """

    pub_key: str
    api_client: APIClient
    headers: dict

    def __init__(self, pub_key: str, mode: MODES = MODES.DEVELOPMENT) -> None:
        self.pub_key = pub_key
        self.api_client = APIClientFactory(mode=mode)
        self.headers = {
            "Authorization": "Bearer %s" % self.pub_key,
            "Content-Type": "application/json",
        }

    # TODO email param -> use `pydantic.EmailStr` requires `email-validator` package
    @pydantic.validate_arguments()
    def create_zainbox(
        self,
        name: str,
        tags: str,
        codeNamePrefix: str,
        callbackUrl: pydantic.AnyHttpUrl,
        email: str,
    ):
        """
        Create a zainbox.
        """

        _create_zainbox_request = self.api_client.send_request(
            method=REQUEST_METHODS.POST,
            url="/zainbox/create/request",
            headers=self.headers,
            data={
                "name": name,
                "tags": tags,
                "codeNamePrefix": codeNamePrefix,
                "callbackUrl": callbackUrl,
                "email": email,
            },
        )

        return _create_zainbox_request

    def list_zainbox(self):
        """
        Get all your created zainboxes
        """

        _list_zainbox_request = self.api_client.send_request(
            method=REQUEST_METHODS.GET,
            url="/zainbox/list",
            headers=self.headers,
        )

        return _list_zainbox_request
