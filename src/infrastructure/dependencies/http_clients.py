from collections.abc import Generator
from typing import Annotated

from fast_depends import Depends

from infrastructure.dependencies.auth_credentials import AccessTokenDependency
from infrastructure.dodo_is_api.http_client import (
    closing_dodo_is_api_http_client,
    DodoIsApiHttpClient,
)
from infrastructure.dependencies.config import ConfigDependency


__all__ = ("get_dodo_is_api_http_client", "DodoIsApiHttpClientDependency")


def get_dodo_is_api_http_client(
    config: ConfigDependency,
    access_token: AccessTokenDependency,
) -> Generator[DodoIsApiHttpClient, None, None]:
    with closing_dodo_is_api_http_client(
        base_url=config.dodo_is_api.base_url,
        access_token=access_token,
    ) as http_client:
        yield http_client


DodoIsApiHttpClientDependency = Annotated[
    DodoIsApiHttpClient,
    Depends(get_dodo_is_api_http_client),
]
