from typing import Annotated

from fast_depends import Depends
from infrastructure.auth_credentials import AuthCredentialsGateway
from infrastructure.dependencies.config import ConfigDependency
from infrastructure.dependencies.service_account import ServiceAccountDependency


__all__ = (
    "get_auth_credentials_gateway",
    "AuthCredentialsGatewayDependency",
    "get_access_token",
    "AccessTokenDependency",
)


def get_auth_credentials_gateway(
    config: ConfigDependency,
    service_account: ServiceAccountDependency,
) -> AuthCredentialsGateway:
    return AuthCredentialsGateway(
        service_account=service_account,
        spreadsheet_id=config.auth_credentials.spreadsheet_id,
        credentials_sheet_id=config.auth_credentials.sheet_id,
    )


AuthCredentialsGatewayDependency = Annotated[
    AuthCredentialsGateway, Depends(get_auth_credentials_gateway)
]


def get_access_token(
    auth_credentials_gateway: AuthCredentialsGatewayDependency,
) -> str:
    return auth_credentials_gateway.get_access_token()


AccessTokenDependency = Annotated[str, Depends(get_access_token)]
