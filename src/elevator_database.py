import sqlite3
from datetime import datetime

from typing import Any
from .db_inteface import DatabaseInterface
from .db_context import DatabaseContext
from .elevator_models import ElevatorColumns


class ElevatorDatabase(DatabaseInterface):
    def __init__(self, database_path: str = "elevator.db") -> None:
        """
        The __init__ function is called when the class is instantiated.
        It sets up the database connection and creates a cursor object to
        execute SQL commands.

        :param database_path: [str] Set the path to the database
        :return: [None]
        """
        self.database_path = database_path
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        """Connect to the database"""
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()

    def close_connection(self) -> None:
        """Close connection with the database"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def _execute_query(
            self, query: str, parameters: tuple = ()) -> None:
        """
        Executes a SQL query on the database.

        :param query:      [str] The SQL query to be executed
        :param parameters: [tuple | None] Optional parameters to be used in
                                          the query
        :return: [None]
        """
        with DatabaseContext(self):
            self.cursor.execute(query, parameters)
            self.connection.commit()

    def _fetch_one(
            self, query: str, parameters: tuple = ()) -> Any:
        """
        Executes a SQL query that is expected to return a single result.

        :param query:      [str] The SQL query to be executed
        :param parameters: [tuple | None] Optional parameters to be used
                                          in the query

        :return: [Any | None] The result of the query, or None if
                              no result is found
        """
        with DatabaseContext(self):
            self.cursor.execute(query, parameters)
            return self.cursor.fetchone()

    def _fetch_all(
            self, query: str, parameters: tuple = ()) -> list | None:
        """
        Executes a SQL query that is expected to return multiple results.

        :param query:      [str] The SQL query to be executed
        :param parameters: [tuple | None] Optional parameters to be used
                                          in the query

        :return: [list | None] A list of tuples representing the results,
                 or None if no results are found
        """
        with DatabaseContext(self):
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()

    def create_table(self) -> None:
        """
        The create_table function creates a table in the database if it does
        not already exist.

        :return: [None]
        """
        query = (
            f"""
                CREATE TABLE IF NOT EXISTS elevator (
                    {ElevatorColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {ElevatorColumns.CURRENT_FLOOR} INTEGER,
                    {ElevatorColumns.DEMAND_FLOOR} INTEGER,
                    {ElevatorColumns.DESTINATION_FLOOR} INTEGER,
                    {ElevatorColumns.CALL_DATETIME} DATETIME DEFAULT
                        CURRENT_TIMESTAMP
                )
            """
        )  # noqa: W291
        self._execute_query(query)

    def recreate_table(self) -> None:
        """
        The recreate_table function drops the elevator table if it exists,
        and then creates a new one.

        :return: [None]
        """
        query = "DROP TABLE IF EXISTS elevator"
        self._execute_query(query)
        self.create_table()

    def insert_call(
        self,
        current_floor: int,
        demand_floor: int,
        destination_floor: int,
        call_datetime: datetime = None
    ) -> None:
        """
        The insert_call function inserts a new row into the elevator table.
        It then uses an SQL query to insert these values into the database.

        :param current_floor:     [int] Store the current floor of the elevator
        :param demand_floor:      [int] Specify the floor that is being called
        :param destination_floor: [int] Specify the floor
        :param call_datetime:     [datetime | None] Specify the date and time
                                                    of the call. If None, the
                                                    current date and time will
                                                    be used.

        :return: [None]
        """
        if call_datetime is None:
            call_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = (
            f"""
                INSERT INTO elevator (
                    {ElevatorColumns.CURRENT_FLOOR},
                    {ElevatorColumns.DEMAND_FLOOR},
                    {ElevatorColumns.DESTINATION_FLOOR},
                    {ElevatorColumns.CALL_DATETIME})
                VALUES (?, ?, ?, ?)
            """
        )
        parameters = (
            current_floor, demand_floor, destination_floor, call_datetime)
        self._execute_query(query, parameters)

    def get_last_floor(self) -> int | None:
        """
        The get_last_floor function returns the last floor
        that the elevator was on.
        If there is no record of a previous floor, it will return None.

        :return: [int] The number of the last floor. [None] otherwise
        """
        query = (
            f"""
            SELECT {ElevatorColumns.DESTINATION_FLOOR}
            FROM elevator
            ORDER BY id DESC
            LIMIT 1
        """
        )

        result = self._fetch_one(query)
        if result:
            return result[0]
        else:
            return None

    def get_all_rows(self) -> list[tuple]:
        """
        The get_all_rows function returns a list of all rows
        in the elevator table.

        :return: [list[tuple]] A list of tuples with the rows
        """
        query = (
            f"""
            SELECT {ElevatorColumns.ID},
                    {ElevatorColumns.CURRENT_FLOOR},
                    {ElevatorColumns.DEMAND_FLOOR},
                    {ElevatorColumns.DESTINATION_FLOOR},
                    {ElevatorColumns.CALL_DATETIME}
            FROM elevator
        """
        )

        result = self._fetch_all(query)
        return result

    def update_column(
            self,
            row_id: int,
            column_name: str,
            column_value: int | datetime
    ) -> None:
        """
        The update_column function updates a specific column in the
        elevator table.

        :param row_id:        [int] Identify the row in the database that will
                                    be updated
        :param column_name:   [str] Name of the column to be updated
        :param column_value:  [int|datetime] New value for the specified column

        :return: [None]
        """
        query = (
            f"""
            UPDATE elevator
            SET {column_name} = ?
            WHERE id = ?
            """
        )
        parameters = (column_value, row_id)

        self._execute_query(query, parameters)

    def row_exists(self, row_id: int) -> bool:
        """
        The row_exists function checks whether a row with the specified 'id'
        exists in the elevator table.

        :param row_id: [int] Identify the row in the database

        :return: [bool] True if the row exists, False otherwise
        """
        query = (
                """
                SELECT COUNT(*)
                FROM elevator
                WHERE id = ?
                """
            )
        parameters = (row_id,)

        count = self._fetch_one(query, parameters)[0]

        return count > 0

    def delete_all_rows(self) -> None:
        """
        The delete_all_rows function deletes all rows in the elevator table.

        :return: [None]
        """
        query = "DELETE FROM elevator"
        self._execute_query(query)


db = ElevatorDatabase()
