class Elevator:
    def __init__(self, db, floors=6):
        self.db = db
        self.floors = floors

    def call_elevator(self, demand_floor, destination_floor):
        current_floor = self.db.get_last_floor()

        if current_floor is None:
            current_floor = demand_floor

        self.db.insert_call(current_floor, demand_floor, destination_floor)
