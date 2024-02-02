import pytest

from src import ElevatorDatabase
from .conftest import TEST_DATABASE_PATH


class TestElevatorDatabase:
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

    def test_execute_query(self, db_instance: ElevatorDatabase) -> None:
        """
        Test the _execute_query method by inserting a row and checking
        if it exists.
        """
        db_instance.recreate_table()
        query = ("""
            INSERT INTO elevator (
                current_floor, demand_floor, destination_floor)
            VALUES (?, ?, ?)
        """)
        parameters = (1, 2, 3)
        db_instance._execute_query(query, parameters)

        query = "SELECT * FROM elevator"
        result = db_instance._fetch_one(query)

        assert result is not None
        assert result[1] == 1
        assert result[2] == 2
        assert result[3] == 3

    def test_fetch_one(self, db_instance: ElevatorDatabase) -> None:
        """
        Test the _fetch_one method by inserting a row and fetching it.
        """
        db_instance.recreate_table()
        db_instance.insert_call(1, 2, 3)

        query = "SELECT * FROM elevator WHERE current_floor = ?"
        parameters = (1,)
        result = db_instance._fetch_one(query, parameters)

        assert result is not None
        assert result[1] == 1
        assert result[2] == 2
        assert result[3] == 3

    def test_fetch_all(self, db_instance: ElevatorDatabase) -> None:
        """
        Test the _fetch_all method by inserting multiple rows and fetching all.
        """
        db_instance.recreate_table()
        db_instance.insert_call(1, 2, 3)
        db_instance.insert_call(4, 5, 6)
        db_instance.insert_call(7, 8, 9)

        query = "SELECT * FROM elevator"
        result = db_instance._fetch_all(query)

        assert result is not None
        assert len(result) == 3

        for row in result:
            assert isinstance(row, tuple)
            assert len(row) == 4

    def test_create_table(self, db_instance: ElevatorDatabase) -> None:
        """Create a table and verify the number of columns"""
        db_instance.create_table()
        query = "PRAGMA table_info('elevator')"
        columns = db_instance._fetch_all(query)
        assert len(columns) == 4

    def test_recreate_table(self, db_instance: ElevatorDatabase) -> None:
        """Recreate the table and verify the number of columns"""
        db_instance.recreate_table()
        query = "PRAGMA table_info('elevator')"
        columns = db_instance._fetch_all(query)
        assert len(columns) == 4

    def test_insert_call(self, db_instance: ElevatorDatabase) -> None:
        """Create a table, insert a call, and verify the inserted values"""
        db_instance.create_table()
        db_instance.insert_call(1, 2, 3)
        query = "SELECT * FROM elevator"
        result = db_instance._fetch_one(query)
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
        db_instance.update_column(
            row_id, 'current_floor', new_current_floor_value)

        query = "SELECT current_floor FROM elevator WHERE id = ?"
        parameters = (row_id,)
        updated_value = db_instance._fetch_one(query, parameters)[0]

        assert updated_value == new_current_floor_value

    def test_row_exists(self, db_instance: ElevatorDatabase) -> None:
        """Create a table, insert a call, and test row existence"""
        db_instance.create_table()
        db_instance.insert_call(1, 2, 3)

        row_id = db_instance.get_all_rows()[-1][0]

        # Test that the row exists
        assert db_instance.row_exists(row_id) is True

        # Test that a non-existing row returns False
        assert db_instance.row_exists(row_id + 1) is False

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

        query = "SELECT COUNT(*) FROM elevator"
        count_after_deletion = db_instance._fetch_one(query)[0]

        assert count_after_deletion == 0
