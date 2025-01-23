from dataclasses import dataclass

from infrastructure.dodo_is_api.connection import DodoIsApiConnection


__all__ = ("DodoIsApiFetchInteractor",)


@dataclass(frozen=True, slots=True, kw_only=True)
class DodoIsApiFetchInteractor:
    dodo_is_api_connection: DodoIsApiConnection
