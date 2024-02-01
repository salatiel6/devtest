import json
import os

from unittest.mock import patch
from flask_testing import TestCase
from src import ElevatorDatabase
from main import app, Elevator, configure_test
from .conftest import TEST_DATABASE_PATH

os.environ["FLASK_ENV"] = "test"


class TestAPI(TestCase):
    db = ElevatorDatabase(TEST_DATABASE_PATH)

    def create_app(self) -> app:
        """
        The create_app function is a factory function that creates the
        Flask application.
        It is called by pytest-flask when it needs to create an app
        for testing.

        :return: [app] A flask app object
        """
        app.config["TESTING"] = True
        configure_test()
        return app

    def setUp(self) -> None:
        """
        Hook method for setting up the test fixture before exercising it.
        """
        self.db.recreate_table()

    def test_health_endpoint(self) -> None:
        """
        Test the health endpoint.
        """
        response = self.client.get("/health")
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert data["status"] == "healthy"

    def test_generate_data_endpoint(self) -> None:
        """
        Test the generate data endpoint.
        """
        with app.app_context():
            response = self.client.get("/generate-data")
            data = json.loads(response.data.decode("utf-8"))
            assert response.status_code == 200
            assert data["message"] == "Data generated successfully"

    def test_generate_data_error(self) -> None:
        """
        Test the generate data endpoint with simulated error.
        """
        with app.app_context():
            with patch("src.DataGenerator.generate",
                       side_effect=Exception("Simulated error")):
                response = self.client.get("/generate-data")

        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 500
        assert "error" in data
        assert "Simulated error" in data["error"]

    def test_call_elevator_endpoint(self) -> None:
        """
        Test the call elevator endpoint.
        """
        data = {"demand_floor": 3, "destination_floor": 5}
        response = self.client.post("/call-elevator", json=data)
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert data["message"] == "Elevator called successfully"

    def test_call_elevator_missing_parameters(self) -> None:
        """
        Test the call elevator endpoint with missing parameters.
        """
        data = {"destination_floor": 5}  # No 'demand_floor'
        response = self.client.post("/call-elevator", json=data)
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert "error" in data
        assert (
                "Both 'demand_floor' and 'destination_floor' are required."
                in data["error"]
        )

    def test_call_elevator_invalid_parameter_type(self) -> None:
        """
        Test the call elevator endpoint with invalid parameter type.
        """
        data = {
            "demand_floor": "invalid",
            "destination_floor": 5,
        }  # 'demand_floor' is not an int
        response = self.client.post("/call-elevator", json=data)
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert "error" in data
        assert (
                "'demand_floor' and 'destination_floor' must be of type int."
                in data["error"]
        )

    def test_get_all_rows_endpoint(self) -> None:
        """
        Test the get all rows endpoint.
        """
        elevator = Elevator(db=self.db)
        elevator.call_elevator(demand_floor=3, destination_floor=5)
        elevator.call_elevator(demand_floor=1, destination_floor=4)

        response = self.client.get("/get-all-rows")
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert len(data) == 2

    def test_get_all_rows_error(self) -> None:
        """
        Test the get all rows endpoint with simulated error.
        """
        with patch("src.ElevatorDatabase.get_all_rows",
                   side_effect=Exception("Simulated error")):
            response = self.client.get("/get-all-rows")

        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 500
        assert "error" in data
        assert "Simulated error" in data["error"]

    def test_update_row_endpoint(self) -> None:
        """
        Test the update row endpoint.
        """
        elevator = Elevator(db=self.db)
        elevator.call_elevator(demand_floor=3, destination_floor=5)

        last_row_id = self.db.get_all_rows()[-1][0]

        update_data = {
            "id": last_row_id,
            "current_floor": 2,
            "demand_floor": 4,
            "destination_floor": 6,
        }

        response = self.client.put("/update-row", json=update_data)
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert data["message"] == f"Row {last_row_id} updated successfully"

        updated_row = self.db.get_all_rows()[-1]
        assert updated_row[0] == last_row_id
        assert updated_row[1] == 2
        assert updated_row[2] == 4
        assert updated_row[3] == 6

    def test_update_row_one_column(self) -> None:
        """
        Test the update row endpoint updating only one column.
        """
        elevator = Elevator(db=self.db)
        elevator.call_elevator(demand_floor=3, destination_floor=5)

        last_row_id = self.db.get_all_rows()[-1][0]

        update_data = {
            "id": last_row_id,
            "demand_floor": 6
        }

        response = self.client.put("/update-row", json=update_data)
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert data["message"] == f"Row {last_row_id} updated successfully"

        updated_row = self.db.get_all_rows()[-1]
        assert updated_row[0] == last_row_id
        assert updated_row[2] == 6

    def test_update_row_missing_id(self) -> None:
        """
        Test the update row endpoint with missing 'id' parameter.
        """
        update_data = {
            "current_floor": 2,
            "demand_floor": 4,
            "destination_floor": 6,
        }

        response = self.client.put("/update-row", json=update_data)
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 400
        assert "error" in data
        assert "Missing parameter 'id'" in data["error"]

    def test_update_row_invalid_id_type(self) -> None:
        """
        Test the update row endpoint with invalid 'id' type.
        """
        update_data = {
            "id": "invalid_id",
            "current_floor": 2,
            "demand_floor": 4,
            "destination_floor": 6,
        }

        response = self.client.put("/update-row", json=update_data)
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 400
        assert "error" in data
        assert "'id' must be of type int." in data["error"]

    def test_update_row_no_valid_column(self) -> None:
        """
        Test the update row endpoint with no valid column provided.
        """
        update_data = {
            "id": 1,  # Valid 'id'
            "invalid_column": 2,  # Invalid column
        }

        response = self.client.put("/update-row", json=update_data)
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 400
        assert "error" in data
        assert "No valid column provided" in data["error"]

    def test_update_row_invalid_column_type(self) -> None:
        """
        Test the update row endpoint with invalid column type.
        """
        update_data = {
            "id": 1,
            "current_floor": "invalid_type",
            # Invalid type for 'current_floor'
        }

        response = self.client.put("/update-row", json=update_data)
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 400
        assert "error" in data
        assert "'current_floor' must be of type int." in data["error"]

    def test_update_row_internal_error(self) -> None:
        """
        Test the update row endpoint with simulated internal error.
        """
        update_data = {
            "id": 1,  # Valid 'id'
            "current_floor": 2,
        }

        # Mock a side effect that raises an exception
        with patch("src.ElevatorDatabase.update_column",
                   side_effect=Exception("Simulated error")):
            response = self.client.put("/update-row", json=update_data)

        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 500
        assert "error" in data
        assert "Simulated error" in data["error"]

    def test_delete_all_rows_endpoint(self) -> None:
        """
        Test the delete all rows endpoint.
        """
        elevator = Elevator(db=self.db)
        elevator.call_elevator(demand_floor=3, destination_floor=5)
        elevator.call_elevator(demand_floor=1, destination_floor=4)

        response = self.client.delete("/delete-all-rows")
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert data["message"] == "All rows deleted successfully"

        rows_after_deletion = self.db.get_all_rows()
        assert len(rows_after_deletion) == 0

    def test_delete_all_rows_internal_error(self) -> None:
        """
        Test the delete all rows endpoint with simulated internal error.
        """
        with patch("src.ElevatorDatabase.delete_all_rows",
                   side_effect=Exception("Simulated error")):
            response = self.client.delete("/delete-all-rows")

        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 500
        assert "error" in data
        assert "Simulated error" in data["error"]

    def test_export_csv_endpoint(self) -> None:
        """
        Test the export CSV endpoint.
        """
        elevator = Elevator(db=self.db)
        elevator.call_elevator(demand_floor=3, destination_floor=5)
        elevator.call_elevator(demand_floor=1, destination_floor=4)

        response = self.client.get("/export-csv")

        assert response.status_code == 200
        assert (
                response.headers["Content-Disposition"]
                == "attachment; filename=elevator_data.csv"
        )
        assert response.headers["Content-Type"] == "text/csv"

        expected_records = [
            "id,current_floor,demand_floor,destination_floor",
            "1,3,3,5",
            "2,5,1,4",
        ]

        actual_csv_content = response.data.decode("utf-8").splitlines()
        for record in expected_records:
            assert record in actual_csv_content

    def test_export_csv_internal_error(self) -> None:
        """
        Test the export CSV endpoint with simulated internal error.
        """
        # Mock a side effect that raises an exception during CSV creation
        with patch("src.ElevatorDatabase.get_all_rows",
                   side_effect=Exception("Simulated error")):
            response = self.client.get("/export-csv")

        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 500
        assert "error" in data
        assert "Simulated error" in data["error"]

    def test_export_csv_response_error(self) -> None:
        """
        Test the export CSV endpoint with simulated response setup error.
        """
        # Mock a side effect that raises an exception during response setup
        with patch("src.ElevatorDatabase.get_all_rows") as mock_get_all_rows:
            mock_get_all_rows.return_value = [
                (1, 2, 3, 4)]  # Ensure some data is returned
            with patch("main.StringIO",
                       side_effect=Exception("Simulated error")):
                response = self.client.get("/export-csv")

        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 500
        assert "error" in data
        assert "Simulated error" in data["error"]
