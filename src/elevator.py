from .db import db


class Elevator:
    def __init__(self, floors=6):
        self.floors = floors
        self.elevator_db = db  # Instância do banco de dados

    def call_elevator(self, demand_floor, destination_floor):
        current_floor = self.elevator_db.get_last_floor()

        if current_floor is None:
            current_floor = demand_floor

        self.elevator_db.insert_call(current_floor, demand_floor, destination_floor)
