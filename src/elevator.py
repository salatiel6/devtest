from .elevator_database import ElevatorDatabase


class Elevator:
    def __init__(self, db: ElevatorDatabase, floors: int = 6) -> None:
        """
        The __init__ function initializes the Elevator instance with a
        database connection and the number of floors.

        :param db:     [ElevatorDatabase] Connect to the database
        :param floors: [int] Set the number of floors in the building

        :return: [None]
        """
        self.db = db
        self.floors = floors

    def call_elevator(self, demand_floor: int, destination_floor: int) -> None:
        """
        The call_elevator function is used to call an elevator from a floor.

        :param demand_floor:      [int] Determine where the elevator is called
                                        from
        :param destination_floor: [int] Determine the direction of the elevator

        :return: [None]
        """
        # Get the last known floor from the database
        current_floor = self.db.get_last_floor()

        # If the current floor is not available, set it to the demanded floor
        if current_floor is None:
            current_floor = demand_floor

        # Insert a call into the database with the
        # current, demand, and destination floors
        self.db.insert_call(current_floor, demand_floor, destination_floor)
