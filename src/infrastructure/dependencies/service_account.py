from typing import Annotated

import gspread
from gspread.client import Client
from fast_depends import Depends

from bootstrap.config import GOOGLE_SHEETS_SERVICE_ACCOUNT_CREDENTIALS_FILE_PATH


__all__ = ("get_service_account", "ServiceAccountDependency")


def get_service_account() -> Client:
    return gspread.service_account(  # type: ignore[reportPrivateImportUsage]
        GOOGLE_SHEETS_SERVICE_ACCOUNT_CREDENTIALS_FILE_PATH
    )


ServiceAccountDependency = Annotated[Client, Depends(get_service_account)]
