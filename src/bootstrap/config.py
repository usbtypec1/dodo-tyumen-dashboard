import tomllib
import pathlib
from typing import Final
from dataclasses import dataclass
from uuid import UUID

import pendulum

from domain.entities import Unit


__all__ = (
    "CONFIG_FILE_PATH",
    "GOOGLE_SHEETS_SERVICE_ACCOUNT_CREDENTIALS_FILE_PATH",
    "DashboardConfig",
    "AuthCredentialsConfig",
    "Config",
    "load_config_from_file",
)


CONFIG_FILE_PATH: Final[pathlib.Path] = (
    pathlib.Path(__file__).parent.parent.parent / "config.toml"
)
GOOGLE_SHEETS_SERVICE_ACCOUNT_CREDENTIALS_FILE_PATH: Final[pathlib.Path] = (
    pathlib.Path(__file__).parent.parent.parent
    / "credentials"
    / "google_sheets_service_account.json"
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DashboardConfig:
    spreadsheet_id: str
    staff_sheet_id: int
    economics_sheet_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthCredentialsConfig:
    spreadsheet_id: str
    sheet_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class DodoIsApiConfig:
    base_url: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    timezone: pendulum.Timezone
    units: list[Unit]
    dashboard: DashboardConfig
    auth_credentials: AuthCredentialsConfig
    dodo_is_api: DodoIsApiConfig


def load_config_from_file(file_path: pathlib.Path = CONFIG_FILE_PATH) -> Config:
    config_text = file_path.read_text("utf-8")
    config = tomllib.loads(config_text)
    
    timezone = pendulum.Timezone(config["app"]["timezone"])
    dashboard = DashboardConfig(
        spreadsheet_id=config["dashboard"]["spreadsheet"]["id"],
        staff_sheet_id=config["dashboard"]["spreadsheet"]["staff_sheet_id"],
        economics_sheet_id=config["dashboard"]["spreadsheet"][
            "economics_sheet_id"
        ],
    )
    auth_credentials = AuthCredentialsConfig(
        spreadsheet_id=config["auth_credentials"]["spreadsheet"]["id"],
        sheet_id=config["auth_credentials"]["spreadsheet"]["sheet_id"],
    )
    dodo_is_api = DodoIsApiConfig(base_url=config["dodo_is_api"]["base_url"])
    units = [
        Unit(uuid=UUID(unit["uuid"]), name=unit["name"])
        for unit in config["auth_credentials"]["units"]
    ]
    return Config(
        timezone=timezone,
        units=units,
        dashboard=dashboard,
        auth_credentials=auth_credentials,
        dodo_is_api=dodo_is_api,
    )
