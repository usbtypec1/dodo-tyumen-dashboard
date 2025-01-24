from typing import Annotated

from fast_depends import Depends

from infrastructure.dependencies.http_clients import (
    DodoIsApiHttpClientDependency,
)
from infrastructure.dodo_is_api.connection import DodoIsApiConnection


__all__ = ("get_dodo_is_api_connection", "DodoIsApiConnectionDependency")


def get_dodo_is_api_connection(
    http_client: DodoIsApiHttpClientDependency,
) -> DodoIsApiConnection:
    return DodoIsApiConnection(http_client=http_client)


DodoIsApiConnectionDependency = Annotated[
    DodoIsApiConnection, Depends(get_dodo_is_api_connection)
]
