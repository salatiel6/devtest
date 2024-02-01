import sqlite3


class ElevatorDatabase:
    def __init__(self, database_path: str = "elevator.db") -> None:
        """
        The __init__ function is called when the class is instantiated.
        It sets up the database connection and creates a cursor object to
        execute SQL commands.

        :param database_path: [str] Set the path to the database
        :return: [None]
        """
        self.database_path = database_path

    def create_table(self) -> None:
        """
        The create_table function creates a table in the database if it does
        not already exist.

        :return: [None]
        """
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS elevator (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        current_floor INTEGER,
                        demand_floor INTEGER,
                        destination_floor INTEGER
                    )
                """
            )

    def recreate_table(self) -> None:
        """
        The recreate_table function drops the elevator table if it exists,
        and then creates a new one.

        :return: [None]
        """
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS elevator")
            self.create_table()

    def insert_call(
        self, current_floor: int, demand_floor: int, destination_floor: int
    ) -> None:
        """
        The insert_call function inserts a new row into the elevator table.
        It then uses an SQL query to insert these values into the database.

        :param current_floor:     [int] Store the current floor of the elevator
        :param demand_floor:      [int] Specify the floor that is being called
        :param destination_floor: [int] Specify the floor

        :return: [None]
        """
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    INSERT INTO elevator (
                        current_floor, demand_floor, destination_floor)
                    VALUES (?, ?, ?)
                """,
                (current_floor, demand_floor, destination_floor),
            )
            connection.commit()

    def get_last_floor(self) -> int | None:
        """
        The get_last_floor function returns the last floor
        that the elevator was on.
        If there is no record of a previous floor, it will return None.

        :return: [int] The number of the last floor. [None] otherwise
        """
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT destination_floor
                FROM elevator
                ORDER BY id DESC
                LIMIT 1
            """
            )
            result = cursor.fetchone()

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
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, current_floor, demand_floor, destination_floor
                FROM elevator
            """
            )
            result = cursor.fetchall()

            return result

    def update_column(
            self, row_id: int, column_name: str, column_value: int) -> None:
        """
        The update_column function updates a specific column in the
        elevator table.

        :param row_id:        [int] Identify the row in the database that will
                                    be updated
        :param column_name:   [str] Name of the column to be updated
        :param column_value:  [int] New value for the specified column

        :return: [None]
        """
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"""
                UPDATE elevator
                SET {column_name} = ?
                WHERE id = ?
                """,
                (column_value, row_id),
            )
            connection.commit()

    def delete_all_rows(self) -> None:
        """
        The delete_all_rows function deletes all rows in the elevator table.

        :return: [None]
        """
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM elevator")
            connection.commit()

    def close_connection(self) -> None:
        """
        The close_connection function closes the connection to the database.

        :return: [None]
        """
        with sqlite3.connect(self.database_path) as connection:
            connection.close()


db = ElevatorDatabase()
