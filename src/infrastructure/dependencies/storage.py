import sqlite3
from typing import Annotated

from fast_depends import Depends

from bootstrap.config import STORAGE_FILE_PATH
from infrastructure.storage import StorageGateway


__all__ = ("get_storage_gateway", "StorageGatewayDependency")


def get_storage_gateway() -> StorageGateway:
    with sqlite3.connect(STORAGE_FILE_PATH) as connection:
        return StorageGateway(connection=connection)


StorageGatewayDependency = Annotated[StorageGateway, Depends(get_storage_gateway)]
