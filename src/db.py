import sqlite3


class ElevatorDatabase:
    def __init__(self, database_path='elevator.db'):
        self.database_path = database_path

    def create_table(self):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS elevator (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    current_floor INTEGER,
                    demand_floor INTEGER,
                    destination_floor INTEGER
                )
            ''')

    def recreate_table(self):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('DROP TABLE IF EXISTS elevator')
            self.create_table()

    def insert_call(self, current_floor, demand_floor, destination_floor):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO elevator (current_floor, demand_floor, destination_floor)
                VALUES (?, ?, ?)
            ''', (current_floor, demand_floor, destination_floor))
            connection.commit()

    def get_last_floor(self):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT destination_floor
                FROM elevator
                ORDER BY id DESC
                LIMIT 1
            ''')
            result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    def get_all_rows(self):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT id, current_floor, demand_floor, destination_floor
                FROM elevator
            ''')
            result = cursor.fetchall()

        return result

    def update_current_floor(self, row_id, current_floor):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE elevator
                SET current_floor = ?
                WHERE id = ?
            ''', (current_floor, row_id))
            connection.commit()

    def update_demand_floor(self, row_id, demand_floor):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE elevator
                SET demand_floor = ?
                WHERE id = ?
            ''', (demand_floor, row_id))
            connection.commit()

    def update_destination_floor(self, row_id, destination_floor):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE elevator
                SET destination_floor = ?
                WHERE id = ?
            ''', (destination_floor, row_id))
            connection.commit()

    def delete_all_rows(self):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM elevator')
            connection.commit()


db = ElevatorDatabase()
