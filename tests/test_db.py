import sqlite3
import pytest

from src import ElevatorDatabase
from .conftest import TEST_DATABASE_PATH


class TestDb:
    @pytest.fixture
    def db_instance(self) -> ElevatorDatabase:
        """
        The db_instance function is a helper function that returns an instance
        of the ElevatorDatabase class. This allows us to use the same database
        for all tests, and also allows us to easily change which database we
        are using.

        :return: [ElevatorDatabase] An instance of the class
        """
        return ElevatorDatabase(TEST_DATABASE_PATH)

    def test_create_table(self, db_instance: ElevatorDatabase) -> None:
        """Create a table and verify the number of columns"""
        db_instance.create_table()
        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info('elevator')")
            columns = cursor.fetchall()
            assert len(columns) == 4

    def test_recreate_table(self, db_instance: ElevatorDatabase) -> None:
        """Recreate the table and verify the number of columns"""
        db_instance.recreate_table()
        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info('elevator')")
            columns = cursor.fetchall()
            assert len(columns) == 4

    def test_insert_call(self, db_instance: ElevatorDatabase) -> None:
        """Create a table, insert a call, and verify the inserted values"""
        db_instance.create_table()
        db_instance.insert_call(1, 2, 3)
        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM elevator")
            result = cursor.fetchone()
            assert result[1] == 1
            assert result[2] == 2
            assert result[3] == 3

    def test_get_last_floor(self, db_instance: ElevatorDatabase) -> None:
        """Create a table, insert a call, and verify the last floor value"""
        db_instance.create_table()
        db_instance.insert_call(1, 2, 3)
        last_floor = db_instance.get_last_floor()
        assert last_floor == 3

    def test_get_all_rows(self, db_instance: ElevatorDatabase) -> None:
        """Create a table, insert multiple calls, and verify all rows"""
        db_instance.create_table()

        db_instance.insert_call(1, 2, 3)
        db_instance.insert_call(4, 5, 6)
        db_instance.insert_call(7, 8, 9)

        rows = db_instance.get_all_rows()

        assert len(rows) > 0

        for row in rows:
            # Verify the structure and types of each row
            assert isinstance(row, tuple)
            assert len(row) == 4
            assert isinstance(row[0], int)
            assert isinstance(row[1], int)
            assert isinstance(row[2], int)
            assert isinstance(row[3], int)

    def test_update_column(self, db_instance: ElevatorDatabase) -> None:
        """
        Create a table, insert a call, update a column,
        and verify the update
        """
        db_instance.create_table()
        db_instance.insert_call(1, 2, 3)
        row_id = db_instance.get_all_rows()[0][0]

        new_current_floor_value = 10
        db_instance.update_column(row_id, 'current_floor',
                                  new_current_floor_value)

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT current_floor FROM elevator WHERE id = ?",
                           (row_id,))
            updated_value = cursor.fetchone()[0]

        assert updated_value == new_current_floor_value

    def test_delete_all_rows(self, db_instance: ElevatorDatabase) -> None:
        """
        Create a table, insert multiple calls, delete all rows,
        and verify deletion
        """
        db_instance.create_table()

        db_instance.insert_call(1, 2, 3)
        db_instance.insert_call(4, 5, 6)
        db_instance.insert_call(7, 8, 9)

        db_instance.delete_all_rows()

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM elevator")
            count_after_deletion = cursor.fetchone()[0]

        assert count_after_deletion == 0
