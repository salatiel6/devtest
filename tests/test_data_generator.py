import os
import json
import sqlite3
import pytest

from src import DataGenerator, ElevatorDatabase, ElevatorColumns
from .conftest import TEST_DATABASE_PATH


class TestDataGenerator:
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

    def test_data_generation(self, db_instance: ElevatorDatabase) -> None:
        """Testing the recreation of the elevator table on testing DB"""

        # Recreate the table and load test data from JSON file
        db_instance.recreate_table()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "../src/elevator_travels.json")

        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                test_data = json.load(file)

        # Generate data and verify the number of rows in the table
        DataGenerator.generate(db_instance)
        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM elevator")
            count_after_generation = cursor.fetchone()[0]

        assert count_after_generation == len(test_data)

        # Verify the generated data matches the test data
        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM elevator")
            rows = cursor.fetchall()

        for i, travel in enumerate(test_data):
            assert rows[i][1] == travel[ElevatorColumns.CURRENT_FLOOR]
            assert rows[i][2] == travel[ElevatorColumns.DEMAND_FLOOR]
            assert rows[i][3] == travel[ElevatorColumns.DESTINATION_FLOOR]
            assert rows[i][4] == travel[ElevatorColumns.CALL_DATETIME]
