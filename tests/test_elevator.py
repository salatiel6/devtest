import pytest

from src import Elevator, ElevatorDatabase
from .conftest import TEST_DATABASE_PATH


class TestElevator:
    @pytest.fixture
    def elevator_instance(self) -> Elevator:
        """
        The elevator_instance function is a fixture that creates an instance
        of the Elevator class.
        It also creates a database and recreates the table in it,
        so that each test starts with an empty database.

        :return: [Elevator] An instance of the class
        """
        db_instance = ElevatorDatabase(TEST_DATABASE_PATH)
        db_instance.recreate_table()

        return Elevator(db=db_instance)

    def test_call_elevator_first_call(
            self, elevator_instance: Elevator) -> None:
        """
        Test that checks if the elevator's last floor is set to 5 after calling
        the call_elevator method with demand floor 3 and destination floor 5.
        """

        elevator_instance.call_elevator(demand_floor=3, destination_floor=5)

        assert elevator_instance.db.get_last_floor() == 5

    def test_call_elevator_subsequent_calls(
            self, elevator_instance: Elevator) -> None:
        """
        Test that checks if the elevator's last floor is set to 4 after calling
        the call_elevator method two times.
        """
        elevator_instance.call_elevator(demand_floor=3, destination_floor=5)
        elevator_instance.call_elevator(demand_floor=1, destination_floor=4)

        assert elevator_instance.db.get_last_floor() == 4
