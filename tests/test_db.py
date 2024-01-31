import sqlite3
import pytest
from src.db import ElevatorDatabase

@pytest.fixture
def db_instance():
    return ElevatorDatabase(':memory:')

def test_create_table(db_instance):
    db_instance.create_table()
    # Verifica se a tabela foi criada corretamente
    with sqlite3.connect(db_instance.database_path) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info('elevator')")
        columns = cursor.fetchall()
        assert len(columns) == 4