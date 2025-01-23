from gspread.client import Client


__all__ = ("AuthCredentialsGateway",)


class AuthCredentialsGateway:
    
    __slots__ = (
        "__spreadsheet",
        "__credentials_sheet",
    )
    
    def __init__(
        self,
        *,
        service_account: Client,
        spreadsheet_id: str,
        credentials_sheet_id: int,
    ) -> None:
        self.__spreadsheet = service_account.open_by_key(spreadsheet_id)
        self.__credentials_sheet = self.__spreadsheet.get_worksheet_by_id(
            credentials_sheet_id
        )
    
    def get_access_token(self) -> str:
        return self.__credentials_sheet.get('A2')[0][0]
