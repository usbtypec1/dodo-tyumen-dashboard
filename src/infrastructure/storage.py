import contextlib
import sqlite3
import datetime
from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities import UnitMonthlyEconomicsData, UnitWeeklyStaffData


__all__ = ("StorageGateway",)


@dataclass(frozen=True, slots=True, kw_only=True)
class StorageGateway:
    connection: sqlite3.Connection

    def __post_init__(self) -> None:
        self.__init_tables()

    def __init_tables(self) -> None:
        queries = (
            """
            CREATE TABLE IF NOT EXISTS units_staff_data (
                unit_name TEXT,
                year INTEGER,
                month INTEGER,
                week INTEGER,
                active_managers_count INTEGER,
                dismissed_managers_count INTEGER,
                active_kitchen_members_count INTEGER,
                dismissed_kitchen_members_count INTEGER,
                active_couriers_count INTEGER,
                dismissed_couriers_count INTEGER,
                active_candidates_count INTEGER,
                dismissed_candidates_count INTEGER,
                new_specialists_count INTEGER,
                active_interns_count INTEGER,
                dismissed_interns_count INTEGER,
                new_candidates_count INTEGER,
                uploaded_at TEXT,
                PRIMARY KEY (unit_name, year, month, week)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS units_economics_data (
                unit_name TEXT,
                year INTEGER,
                month INTEGER,
                sales INTEGER,
                delivery_orders_count INTEGER,
                sales_per_person REAL,
                orders_per_courier REAL,
                uploaded_at TEXT,
                PRIMARY KEY (unit_name, year, month)
            )
            """,
        )
        for query in queries:
            with self.connection:
                self.connection.execute(query)
                self.connection.commit()

    def add_units_staff_data(self, units_data: Iterable[UnitWeeklyStaffData]) -> None:
        query = """
        INSERT INTO units_staff_data (
            unit_name,
            year,
            month,
            week,
            active_managers_count,
            dismissed_managers_count,
            active_kitchen_members_count,
            dismissed_kitchen_members_count,
            active_couriers_count,
            dismissed_couriers_count,
            active_candidates_count,
            dismissed_candidates_count,
            new_specialists_count,
            active_interns_count,
            dismissed_interns_count,
            new_candidates_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        rows = [
            (
                unit_data.unit_name,
                unit_data.year,
                unit_data.month,
                unit_data.week,
                unit_data.active_managers_count,
                unit_data.dismissed_managers_count,
                unit_data.active_kitchen_members_count,
                unit_data.dismissed_kitchen_members_count,
                unit_data.active_couriers_count,
                unit_data.dismissed_couriers_count,
                unit_data.active_candidates_count,
                unit_data.dismissed_candidates_count,
                unit_data.new_specialists_count,
                unit_data.active_interns_count,
                unit_data.dismissed_interns_count,
                unit_data.new_candidates_count,
            )
            for unit_data in units_data
        ]
        with self.connection:
            self.connection.executemany(query, rows)

    def add_units_economics_data(
        self, units_data: Iterable[UnitMonthlyEconomicsData]
    ) -> None:
        query = """
        INSERT INTO units_economics_data (
            unit_name,
            year,
            month,
            sales,
            delivery_orders_count,
            sales_per_person,
            orders_per_courier
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        rows = [
            (
                unit_data.unit_name,
                unit_data.year,
                unit_data.month,
                unit_data.sales,
                unit_data.delivery_orders_count,
                unit_data.sales_per_person,
                unit_data.orders_per_courier,
            )
            for unit_data in units_data
        ]
        with self.connection:
            self.connection.executemany(query, rows)

    def get_unuploaded_units_economics_data(
        self,
    ) -> list[UnitMonthlyEconomicsData]:
        query = """
        SELECT
            unit_name,
            year,
            month,
            sales,
            delivery_orders_count,
            sales_per_person,
            orders_per_courier
        FROM units_economics_data
        WHERE
            uploaded_at IS NULL
        ORDER BY year, month, unit_name;
        """
        cursor = self.connection.cursor()
        with contextlib.closing(cursor):
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            UnitMonthlyEconomicsData(
                unit_name=unit_name,
                year=year,
                month=month,
                sales=sales,
                delivery_orders_count=delivery_orders_count,
                sales_per_person=sales_per_person,
                orders_per_courier=orders_per_courier,
            )
            for unit_name, year, month, sales, delivery_orders_count, sales_per_person, orders_per_courier in rows
        ]

    def get_unuploaded_staff_data(self) -> list[UnitWeeklyStaffData]:
        query = """
        SELECT
            unit_name,
            year,
            month,
            week,
            active_managers_count,
            dismissed_managers_count,
            active_kitchen_members_count,
            dismissed_kitchen_members_count,
            active_couriers_count,
            dismissed_couriers_count,
            active_candidates_count,
            dismissed_candidates_count,
            new_specialists_count,
            active_interns_count,
            dismissed_interns_count,
            new_candidates_count
        FROM units_staff_data
        WHERE
            uploaded_at IS NULL
        ORDER BY year, month, week, unit_name;
        """
        cursor = self.connection.cursor()
        with contextlib.closing(cursor):
            cursor.execute(query)
            rows = cursor.fetchall()
        return [
            UnitWeeklyStaffData(
                unit_name=unit_name,
                year=year,
                month=month,
                week=week,
                active_managers_count=active_managers_count,
                dismissed_managers_count=dismissed_managers_count,
                active_kitchen_members_count=active_kitchen_members_count,
                dismissed_kitchen_members_count=dismissed_kitchen_members_count,
                active_couriers_count=active_couriers_count,
                dismissed_couriers_count=dismissed_couriers_count,
                active_candidates_count=active_candidates_count,
                dismissed_candidates_count=dismissed_candidates_count,
                new_specialists_count=new_specialists_count,
                active_interns_count=active_interns_count,
                dismissed_interns_count=dismissed_interns_count,
                new_candidates_count=new_candidates_count,
            )
            for unit_name, year, month, week, active_managers_count, dismissed_managers_count, active_kitchen_members_count, dismissed_kitchen_members_count, active_couriers_count, dismissed_couriers_count, active_candidates_count, dismissed_candidates_count, new_specialists_count, active_interns_count, dismissed_interns_count, new_candidates_count in rows
        ]

    def mark_units_economics_data_as_uploaded(
        self, units_data: Iterable[UnitMonthlyEconomicsData]
    ) -> None:
        now = datetime.datetime.now(datetime.UTC).isoformat()
        query = "UPDATE units_economics_data SET uploaded_at = ? WHERE unit_name = ? AND year = ? AND month = ?;"
        params = [
            (now, unit_data.unit_name, unit_data.year, unit_data.month)
            for unit_data in units_data
        ]
        with self.connection:
            cursor = self.connection.cursor()
            with contextlib.closing(cursor):
                cursor.executemany(query, params)

    def mark_units_staff_data_as_uploaded(
        self,
        units_data: Iterable[UnitWeeklyStaffData],
    ) -> None:
        now = datetime.datetime.now(datetime.UTC).isoformat()
        query = "UPDATE units_staff_data SET uploaded_at = ? WHERE unit_name = ? AND year = ? AND month = ?;"
        params = [
            (now, unit_data.unit_name, unit_data.year, unit_data.month)
            for unit_data in units_data
        ]
        with self.connection:
            cursor = self.connection.cursor()
            with contextlib.closing(cursor):
                cursor.executemany(query, params)
