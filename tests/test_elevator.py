import pytest
from src import Elevator, ElevatorDatabase


class TestElevator:
    @pytest.fixture
    def db_instance(self):
        return ElevatorDatabase(database_path='elevator_test.db')

    @pytest.fixture
    def elevator_instance(self, db_instance):
        db_instance.recreate_table()

        return Elevator(db=db_instance)

    def test_call_elevator_first_call(self, elevator_instance):
        elevator_instance.call_elevator(demand_floor=3, destination_floor=5)

        assert elevator_instance.db.get_last_floor() == 5

    def test_call_elevator_subsequent_calls(self, elevator_instance):
        elevator_instance.call_elevator(demand_floor=3, destination_floor=5)
        elevator_instance.call_elevator(demand_floor=1, destination_floor=4)

        assert elevator_instance.db.get_last_floor() == 4
