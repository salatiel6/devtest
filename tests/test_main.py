import json
import os
from flask_testing import TestCase
from src import ElevatorDatabase
from main import app, Elevator, configure_test

os.environ["FLASK_ENV"] = "test"


class TestAPI(TestCase):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(script_dir, "./elevator_test.db")
    db = ElevatorDatabase(database_path=database_path)

    def create_app(self):
        app.config["TESTING"] = True
        configure_test()
        return app

    def setUp(self):
        self.db.recreate_table()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert data["status"] == "healthy"

    def test_generate_data_endpoint(self):
        with app.app_context():
            response = self.client.get("/generate-data")
            data = json.loads(response.data.decode("utf-8"))
            assert response.status_code == 200
            assert data["message"] == "Data generated successfully"

    def test_call_elevator_endpoint(self):
        data = {"demand_floor": 3, "destination_floor": 5}
        response = self.client.post("/call-elevator", json=data)
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        assert data["message"] == "Elevator called successfully"

    def test_get_all_rows_endpoint(self):
        elevator = Elevator(db=self.db)
        elevator.call_elevator(demand_floor=3, destination_floor=5)
        elevator.call_elevator(demand_floor=1, destination_floor=4)

        response = self.client.get("/get-all-rows")
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert len(data) == 2

    def test_update_row_endpoint(self):
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

    def test_delete_all_rows_endpoint(self):
        elevator = Elevator(db=self.db)
        elevator.call_elevator(demand_floor=3, destination_floor=5)
        elevator.call_elevator(demand_floor=1, destination_floor=4)

        response = self.client.delete("/delete-all-rows")
        data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert data["message"] == "All rows deleted successfully"

        rows_after_deletion = self.db.get_all_rows()
        assert len(rows_after_deletion) == 0

    def test_export_csv_endpoint(self):
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
