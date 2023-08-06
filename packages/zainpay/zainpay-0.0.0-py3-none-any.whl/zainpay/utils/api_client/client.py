import requests
from circuitbreaker import circuit

from zainpay.utils.constants import REQUEST_METHODS


class APIClient:

    base_url: str | None

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url

    def join_url(self, *urls: str | None) -> str:
        _urls: list[str] = []

        for url in urls:
            if url is not None:
                if url.startswith("/"):
                    url = url[1:]
                if url.endswith("/"):
                    url = url[:-1]
                _urls.append(url)

        return "/".join(_urls) + "/"

    @circuit
    def send_request(
        self,
        method: REQUEST_METHODS,
        url: str,
        headers: dict | None = None,
        data: dict | None = None,
        *args: list | tuple,
        **kwargs: dict,
    ) -> requests.Response:
        try:
            url = self.join_url(self.base_url, url)

            return requests.request(
                method,
                url,
                headers=headers,
                data=data,
                *args,
                **kwargs,
            )
        except Exception as error:
            raise error
