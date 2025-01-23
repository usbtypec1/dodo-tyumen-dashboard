import httpx


__all__ = (
    "ResponseStatusCodeError",
    "ResponseJsonParseError",
    "ResponseJsonInvalidTypeError",
    "ResponseDataParseError",
)


class ResponseStatusCodeError(Exception):
    """Raised when the response status code is not successful."""

    def __init__(self, response: httpx.Response) -> None:
        super().__init__(f"Response status code is not successful: {response.status_code} - {response.text}")
        self.response = response


class ResponseJsonParseError(Exception):
    def __init__(self, response: httpx.Response) -> None:
        super().__init__("Could not decode response JSON")
        self.response = response


class ResponseJsonInvalidTypeError(Exception):
    """Raised when the response JSON is not of the expected type.

    For example, expected dict, but list given and vice versa.
    """

    def __init__(self) -> None:
        super().__init__("Response JSON is not of the expected type")


class ResponseDataParseError(Exception):
    """Raised when the response data is not in the expected format.

    For example, missing required keys.
    """

    def __init__(self, response_data: dict | list) -> None:
        super().__init__("Response data is not in the expected format")
        self.response_data = response_data
