from .db import db


class DataGenerator:
    @staticmethod
    def generate():
        data = [
            (1, 2, 1),
            (1, 3, 1),
            (1, 4, 1),
            (1, 5, 1),
            (1, 6, 1),
            (1, 1, 2),
            (2, 1, 3),
            (3, 1, 4),
            (4, 1, 5),
            (5, 1, 6)
        ]

        for current_floor, demand_floor, destination_floor in data:
            db.insert_call(current_floor, demand_floor, destination_floor)
