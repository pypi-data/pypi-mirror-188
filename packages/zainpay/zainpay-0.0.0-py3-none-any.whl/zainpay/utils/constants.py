import enum


class REQUEST_METHODS(str, enum.Enum):

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class MODES(str, enum.Enum):

    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"


DEVELOPMENT_URL: str = "https://sandbox.zainpay.ng/"
PRODUCTION_URL: str = "https://api.zainpay.ng/"
