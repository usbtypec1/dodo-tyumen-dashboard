from collections.abc import Iterable
from uuid import UUID
from dataclasses import dataclass
from itertools import batched

from application.interactors.dodo_is_api_fetch import DodoIsApiFetchInteractor
from infrastructure.dodo_is_api.models import StaffPositionsHistory
from infrastructure.dodo_is_api.response_parsers import (
    parse_staff_positions_history_response,
)
from bootstrap.logger import create_logger


__all__ = ("StaffPositionsHistoryFetchInteractor",)


logger = create_logger("fetch_interactors")


@dataclass(frozen=True, slots=True, kw_only=True)
class StaffPositionsHistoryFetchInteractor(DodoIsApiFetchInteractor):
    staff_member_ids: Iterable[UUID]

    def execute(self) -> list[StaffPositionsHistory]:
        take: int = 1000
        skip: int = 0

        batch_size: int = 30
        staff_members_ids_batches = batched(self.staff_member_ids, n=batch_size)

        history: list[StaffPositionsHistory] = []

        for batch_number, staff_member_ids_batch in enumerate(
            staff_members_ids_batches, start=1
        ):
            while True:
                response = self.dodo_is_api_connection.get_staff_positions_history(
                    staff_member_ids=staff_member_ids_batch,
                    take=take,
                    skip=skip,
                )
                staff_positions_history_response = (
                    parse_staff_positions_history_response(response)
                )

                history += staff_positions_history_response.history

                logger.debug(
                    "staff positions history page fetched: batch number - %d, taken - %d, skipped - %d",
                    batch_number,
                    len(staff_positions_history_response.history),
                    skip,
                )

                if staff_positions_history_response.is_end_of_list_reached:
                    break

                skip += take

            logger.debug(
                "Staff positions history batch fetched: batch number - %d",
                batch_number,
            )

        logger.info(
            "Staff positions history fetching finished: total count - %d",
            len(history),
        )

        return history
