import os
import json
import sqlite3
import pytest
from src import DataGenerator, ElevatorDatabase


class TestDataGenerator:
    @pytest.fixture
    def db_instance(self):
        return ElevatorDatabase(database_path="elevator_test.db")

    def test_data_generation(self, db_instance):
        db_instance.recreate_table()

        script_dir = os.path.dirname(os.path.abspath(__file__))

        json_path = os.path.join(script_dir, "../src/elevator_travels.json")

        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                test_data = json.load(file)

        DataGenerator.generate(db_instance)

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM elevator")
            count_after_generation = cursor.fetchone()[0]

        assert count_after_generation == len(test_data)

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM elevator")
            rows = cursor.fetchall()

        for i, travel in enumerate(test_data):
            assert rows[i][1] == travel["current_floor"]
            assert rows[i][2] == travel["demand_floor"]
            assert rows[i][3] == travel["destination_floor"]
