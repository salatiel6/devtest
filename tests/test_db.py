import sqlite3
import time

import pytest
from src import ElevatorDatabase


class TestDb:
    @pytest.fixture
    def db_instance(self):
        return ElevatorDatabase(database_path='elevator_test.db')

    def test_create_table(self, db_instance):
        db_instance.create_table()
        time.sleep(0.1)
        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info('elevator')")
            columns = cursor.fetchall()
            assert len(columns) == 4

    def test_recreate_table(self, db_instance):
        db_instance.recreate_table()
        time.sleep(0.1)
        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info('elevator')")
            columns = cursor.fetchall()
            assert len(columns) == 4

    def test_insert_call(self, db_instance):
        db_instance.create_table()
        db_instance.insert_call(1, 2, 3)
        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM elevator')
            result = cursor.fetchone()
            assert result[1] == 1
            assert result[2] == 2
            assert result[3] == 3

    def test_get_last_floor(self, db_instance):
        db_instance.create_table()
        db_instance.insert_call(1, 2, 3)
        last_floor = db_instance.get_last_floor()
        assert last_floor == 3

    def test_get_all_rows(self, db_instance):
        db_instance.create_table()

        db_instance.insert_call(1, 2, 3)
        db_instance.insert_call(4, 5, 6)
        db_instance.insert_call(7, 8, 9)

        rows = db_instance.get_all_rows()

        assert len(rows) > 0

        for row in rows:
            assert isinstance(row, tuple)
            assert len(row) == 4
            assert isinstance(row[0], int)
            assert isinstance(row[1], int)
            assert isinstance(row[2], int)
            assert isinstance(row[3], int)

    def test_update_current_floor(self, db_instance):
        db_instance.create_table()

        db_instance.insert_call(1, 2, 3)

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT MAX(id) FROM elevator')
            row_id = cursor.fetchone()[0]

        new_current_floor = 10
        db_instance.update_current_floor(row_id, new_current_floor)

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT current_floor FROM elevator WHERE id = {row_id}')
            updated_current_floor = cursor.fetchone()[0]

        assert updated_current_floor == new_current_floor

    def test_update_demand_floor(self, db_instance):
        db_instance.create_table()

        db_instance.insert_call(1, 2, 3)

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT MAX(id) FROM elevator')
            row_id = cursor.fetchone()[0]

        new_demand_floor = 20
        db_instance.update_demand_floor(row_id, new_demand_floor)

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT demand_floor FROM elevator WHERE id = {row_id}')
            updated_demand_floor = cursor.fetchone()[0]

        assert updated_demand_floor == new_demand_floor

    def test_update_destination_floor(self, db_instance):
        db_instance.create_table()

        db_instance.insert_call(1, 2, 3)

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT MAX(id) FROM elevator')
            row_id = cursor.fetchone()[0]

        new_destination_floor = 30
        db_instance.update_destination_floor(row_id, new_destination_floor)

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT destination_floor FROM elevator WHERE id = {row_id}')
            updated_destination_floor = cursor.fetchone()[0]

        assert updated_destination_floor == new_destination_floor

    def test_delete_all_rows(self, db_instance):
        db_instance.create_table()

        db_instance.insert_call(1, 2, 3)
        db_instance.insert_call(4, 5, 6)
        db_instance.insert_call(7, 8, 9)

        db_instance.delete_all_rows()

        with sqlite3.connect(db_instance.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM elevator')
            count_after_deletion = cursor.fetchone()[0]

        assert count_after_deletion == 0
