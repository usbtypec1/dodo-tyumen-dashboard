import contextlib
from collections.abc import Generator
from typing import NewType

import httpx


__all__ = ("DodoIsApiHttpClient", "closing_dodo_is_api_http_client")


DodoIsApiHttpClient = NewType("DodoIsApiHttpClient", httpx.Client)


@contextlib.contextmanager
def closing_dodo_is_api_http_client(
    *,
    base_url: str,
    access_token: str,
    timeout: int = 120,
) -> Generator[DodoIsApiHttpClient, None, None]:
    headers = {"Authorization": f"Bearer {access_token}"}
    with httpx.Client(
        base_url=base_url,
        headers=headers,
        timeout=timeout,
    ) as http_client:
        yield DodoIsApiHttpClient(http_client)
