import os
import csv
from datetime import datetime

from flask import Flask, jsonify, request, make_response
from io import StringIO
from http import HTTPStatus
from src import Elevator, DataGenerator, ElevatorDatabase, ElevatorColumns
from tests import TEST_DATABASE_PATH

# Create a Flask application
app = Flask(__name__)
# Initialize the database
db: ElevatorDatabase


def setup() -> None:
    """
    Initial application configuration.

    This function is called before running the Flask application and is
    responsible to perform any necessary configuration, such as creating and
    database initialization.

    :return: [None]
    """
    global db
    db_file_path = "./elevator.db"

    if not os.path.exists(db_file_path):
        db = ElevatorDatabase()
        db.create_table()
        data_generator = DataGenerator()
        data_generated = data_generator.generate(db)

        if not data_generated:
            print("Error while generating data")
    else:
        db = ElevatorDatabase(db_file_path)


setup()


@app.route("/health", methods=["GET"])
def health():
    """
    The health function is used to check the health of the API.

    :return: A success message with OK code if it's everything working.
             Error INTERNAL_SERVER_ERROR otherwise
    """
    try:
        return jsonify({"status": "healthy"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/generate-data", methods=["GET"])
def generate_data():
    """
    The generate_data function is used to generate data for the database.
    It will recreate the table and then use DataGenerator to generate data.

    :return: A success message with OK code if it's everything working.
             An Error BAD_REQUEST if there's some problem with the request
             Error INTERNAL_SERVER_ERROR otherwise
    """
    try:
        with app.app_context():
            # generate data using DataGenerator
            _data_generator = DataGenerator()
            _data_generated = _data_generator.generate(db)

            if _data_generated:
                return jsonify({
                    "message": "Data generated successfully"}), HTTPStatus.OK
            else:
                return jsonify({
                    "error": "Error while generating data. "
                             "Check if elevator_travels.json file exists"
                }), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/call-elevator", methods=["POST"])
def call_elevator():
    """
    The call_elevator function is used to call an elevator from a given floor.
    The function takes two parameters: demand_floor and destination_floor.
    The demand_floor parameter represents the floor where the user is located,
    while the destination_floor parameter represents the desired final
    location of that user.

    :return: A success message with OK code if it's everything working.
             An Error BAD_REQUEST if there's some problem with the request
             Error INTERNAL_SERVER_ERROR otherwise
    """
    try:
        data = request.get_json()

        # Validate presence of required parameters
        if (
                ElevatorColumns.DEMAND_FLOOR not in data
                or ElevatorColumns.DESTINATION_FLOOR not in data):
            return jsonify({
                "error": f"Both '{ElevatorColumns.DEMAND_FLOOR}' and "
                         f"'{ElevatorColumns.DESTINATION_FLOOR}' are required."
            }), HTTPStatus.BAD_REQUEST

        # Validate types of parameters
        demand_floor = data[ElevatorColumns.DEMAND_FLOOR]
        destination_floor = data[ElevatorColumns.DESTINATION_FLOOR]

        if not isinstance(demand_floor, int) or not isinstance(
                destination_floor, int):
            return jsonify({
                "error": f"'{ElevatorColumns.DEMAND_FLOOR}' and "
                         f"'{ElevatorColumns.DESTINATION_FLOOR}' must be of "
                         f"type int."
            }), HTTPStatus.BAD_REQUEST

        with app.app_context():
            # Create an Elevator instance and call the elevator
            elevator = Elevator(db)
            elevator.call_elevator(demand_floor, destination_floor)

        return jsonify({
            "message": "Elevator called successfully"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/get-all-rows", methods=["GET"])
def get_all_rows():
    """
    The get_all_rows function retrieves all rows from the database and
    formats them into a JSON object.

    :return: A success message with OK code if it's everything working.
             An Error BAD_REQUEST if there's some problem with the request
             Error INTERNAL_SERVER_ERROR otherwise
    """
    try:
        with app.app_context():
            # Retrieve all rows from the database and format the result
            rows = db.get_all_rows()
            result = [
                {
                    f"{ElevatorColumns.ID}": row[0],
                    f"{ElevatorColumns.CURRENT_FLOOR}": row[1],
                    f"{ElevatorColumns.DEMAND_FLOOR}": row[2],
                    f"{ElevatorColumns.DESTINATION_FLOOR}": row[3],
                    f"{ElevatorColumns.CALL_DATETIME}": row[4]
                }
                for row in rows
            ]

            return jsonify(result), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/update-row", methods=["PUT"])
def update_row():
    """
    The update_row function is used to update the values of a row
    in the database.
    It takes a JSON object with an 'id' field and one or more fields from:
        - current_floor:     [int]
        - demand_floor:      [int]
        - destination_floor: [int]
        - call_datetime:     [str] (in the format YYYY-MM-DD HH:MM:SS)

    :return: A success message with OK code if it's everything working.
             An Error BAD_REQUEST if there's some problem with the request
             Error INTERNAL_SERVER_ERROR otherwise
    """
    try:
        data = request.get_json()

        # Validate presence of required parameters
        if ElevatorColumns.ID not in data:
            return (
                jsonify({
                    "error": f"Missing parameter '{ElevatorColumns.ID}'"}),
                HTTPStatus.BAD_REQUEST
            )

        # Validate type of 'id' parameter
        row_id = data[ElevatorColumns.ID]
        if not isinstance(row_id, int):
            return (
                jsonify({
                    "error": f"'{ElevatorColumns.ID}' must be of type int."}),
                HTTPStatus.BAD_REQUEST
            )

        # Check if the row with the provided 'id' exists
        if not db.row_exists(row_id):
            return (
                jsonify({
                    "error": f"Invalid '{ElevatorColumns.ID}': {row_id}"}),
                HTTPStatus.BAD_REQUEST
            )

        # Set the allowed columns
        allowed_columns = {
            f"{ElevatorColumns.CURRENT_FLOOR}",
            f"{ElevatorColumns.DEMAND_FLOOR}",
            f"{ElevatorColumns.DESTINATION_FLOOR}",
            f"{ElevatorColumns.CALL_DATETIME}"
        }

        # Filters the columns caught on the request
        update_dict = {
            col: data[col] for col in allowed_columns if col in data}

        # Validate the columns types
        for column_name, column_value in update_dict.items():
            if column_name == ElevatorColumns.CALL_DATETIME:
                # Ensure the datetime format is correct
                try:
                    datetime.strptime(column_value, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    return (
                        jsonify({
                            "error": f"Invalid "
                                     f"'{ElevatorColumns.CALL_DATETIME}' "
                                     f"format."
                        }),
                        HTTPStatus.BAD_REQUEST
                    )
            elif not isinstance(column_value, int):
                return (
                    jsonify({
                        "error": f"'{column_name}' must be of type int or "
                                 f"'{ElevatorColumns.CALL_DATETIME}' must be "
                                 f"in the format 'YYYY-MM-DD HH:MM:SS'."}),
                    HTTPStatus.BAD_REQUEST
                )

        # Update the columns on db
        if update_dict:
            for column_name, column_value in update_dict.items():
                db.update_column(row_id, column_name, column_value)

            return (
                jsonify({
                    "message": f"Row {row_id} updated successfully"}),
                HTTPStatus.OK
            )
        else:
            return jsonify(
                {"error": "No valid column provided"}), HTTPStatus.BAD_REQUEST

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/delete-all-rows", methods=["DELETE"])
def delete_all_rows():
    """
    The delete_all_rows function deletes all rows from the database.

    :return: A success message with OK code if it's everything working.
             An Error BAD_REQUEST if there's some problem with the request
             Error INTERNAL_SERVER_ERROR otherwise
    """
    try:
        with app.app_context():
            # Delete all rows from the database
            db.delete_all_rows()
        return jsonify(
            {"message": "All rows deleted successfully"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/export-csv", methods=["GET"])
def export_csv():
    """
    The export_csv function is used to export the data from the database
    into a CSV file.
    The function first retrieves all rows from the database and creates a
    StringIO object that will be used as an in-memory buffer
    for writing CSV data.
    A csv_writer object is created using this StringIO object, which writes
    each row of data to it. The header row is written first,
    followed by all other rows of elevator information.

    :return: A CSV file with the data from the database
    """
    try:
        with app.app_context():
            # Retrieve all rows and create a CSV file
            rows = db.get_all_rows()
            csv_data = StringIO()
            csv_writer = csv.writer(csv_data)

            # Write the header
            csv_writer.writerow([
                f"{ElevatorColumns.ID}",
                f"{ElevatorColumns.CURRENT_FLOOR}",
                f"{ElevatorColumns.DEMAND_FLOOR}",
                f"{ElevatorColumns.DESTINATION_FLOOR}",
                f"{ElevatorColumns.CALL_DATETIME}"
            ])

            # Write the data
            csv_writer.writerows(rows)

            csv_data.seek(0)

        # Set up the response with CSV content
        response = make_response(csv_data.getvalue())
        response.headers[
            "Content-Disposition"
        ] = "attachment; filename=elevator_data.csv"
        response.headers["Content-Type"] = "text/csv"

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


def configure_test() -> None:
    """
    The configure_test function is used to configure the database for testing
    purposes.
    It sets up a new database with the name elevator_test.db in the tests
    directory, and then sets that as our global db variable so that we can
    use it throughout our test suite.

    :return: [None]
    """
    global db
    db = ElevatorDatabase(TEST_DATABASE_PATH)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
