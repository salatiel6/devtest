import os
import json

from .elevator_database import ElevatorDatabase


class DataGenerator:
    @staticmethod
    def generate(db: ElevatorDatabase) -> bool:
        """
        The generate function will load data from the JSON file and insert it
        into the database.

        :param db: Access the database
        :return: The number of rows inserted into the database
        :doc-author: Trelent
        """
        # Get the current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the full path for the JSON file
        json_path = os.path.join(script_dir, "elevator_travels.json")

        # Check if the file exists before trying to open it
        if os.path.exists(json_path):
            # Load data from the JSON file
            with open(json_path, "r") as file:
                data = json.load(file)

            # Iterate over the data and insert into the database
            for travel in data:
                current_floor = travel["current_floor"]
                demand_floor = travel["demand_floor"]
                destination_floor = travel["destination_floor"]
                call_datetime = travel["call_datetime"]

                db.insert_call(
                    current_floor,
                    demand_floor,
                    destination_floor,
                    call_datetime
                )

            return True
        else:
            return False
