import csv

from flask import Flask, jsonify, request, make_response
from io import StringIO
from src import Elevator, DataGenerator, ElevatorDatabase
from tests import TEST_DATABASE_PATH

# Create a Flask application
app = Flask(__name__)
# Initialize the database
db = ElevatorDatabase()


@app.route("/health", methods=["GET"])
def health():
    """
    The health function is used to check the health of the API.

    :return: A success message with 200 code if it's everything working.
             Error 500 otherwise
    """
    try:
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate-data", methods=["GET"])
def generate_data():
    """
    The generate_data function is used to generate data for the database.
    It will recreate the table and then use DataGenerator to generate data.

    :return: A success message with 200 code if it's everything working.
             Error 500 otherwise
    """
    try:
        with app.app_context():
            # Recreate the table and generate data using DataGenerator
            db.recreate_table()
            data_generator = DataGenerator()
            data_generator.generate(db)

        return jsonify({"message": "Data generated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/call-elevator", methods=["POST"])
def call_elevator():
    """
    The call_elevator function is used to call an elevator from a given floor.
    The function takes two parameters: demand_floor and destination_floor.
    The demand_floor parameter represents the floor where the user is located,
    while the destination_floor parameter represents the desired final
    location of that user.

    :return: A success message with 200 code if it's everything working.
             An Error 400 if there's some problem with the request
             Error 500 otherwise
    """
    try:
        data = request.get_json()

        # Validate presence of required parameters
        if "demand_floor" not in data or "destination_floor" not in data:
            return jsonify({
                "error": "Both 'demand_floor' and 'destination_floor' "
                "are required."
            }), 400,

        # Validate types of parameters
        demand_floor = data["demand_floor"]
        destination_floor = data["destination_floor"]

        if not isinstance(demand_floor, int) or not isinstance(
                destination_floor, int):
            return jsonify({
                "error": "'demand_floor' and 'destination_floor' "
                         "must be of type int."
            }), 400,

        with app.app_context():
            # Create an Elevator instance and call the elevator
            elevator = Elevator(db)
            elevator.call_elevator(demand_floor, destination_floor)

        return jsonify({"message": "Elevator called successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get-all-rows", methods=["GET"])
def get_all_rows():
    """
    The get_all_rows function retrieves all rows from the database and
    formats them into a JSON object.

    :return: A success message with 200 code if it's everything working.
             An Error 400 if there's some problem with the request
             Error 500 otherwise
    """
    try:
        with app.app_context():
            # Retrieve all rows from the database and format the result
            rows = db.get_all_rows()
            result = [
                {
                    "id": row[0],
                    "current_floor": row[1],
                    "demand_floor": row[2],
                    "destination_floor": row[3],
                }
                for row in rows
            ]

            return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update-row", methods=["PUT"])
def update_row():
    """
    The update_row function is used to update the values of a row
    in the database.
    It takes a JSON object with an 'id' field and one or more fields from:
        - current_floor:     [int]
        - demand_floor:      [int]
        - destination_floor: [int]

    :return: A success message with 200 code if it's everything working.
             An Error 400 if there's some problem with the request
             Error 500 otherwise
    """
    try:
        data = request.get_json()

        # Validate presence of required parameters
        if "id" not in data:
            return jsonify({"error": "Missing parameter 'id'"}), 400

        # Validate type of 'id' parameter
        row_id = data["id"]
        if not isinstance(row_id, int):
            return jsonify({"error": "'id' must be of type int."}), 400

        # Set the allowed columns
        allowed_columns = {
            "current_floor", "demand_floor", "destination_floor"}

        # Filters the columns caught on the request
        update_dict = {
            col: data[col] for col in allowed_columns if col in data}

        # Validate the columns types
        for column_name, column_value in update_dict.items():
            if not isinstance(column_value, int):
                return jsonify({
                    "error": f"'{column_name}' must be of type int."}), 400

        # Update the columns on db
        if update_dict:
            for column_name, column_value in update_dict.items():
                db.update_column(row_id, column_name, column_value)

            return jsonify({
                "message": f"Row {row_id} updated successfully"}), 200
        else:
            return jsonify({"error": "No valid column provided"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete-all-rows", methods=["DELETE"])
def delete_all_rows():
    """
    The delete_all_rows function deletes all rows from the database.

    :return: A success message with 200 code if it's everything working.
             An Error 400 if there's some problem with the request
             Error 500 otherwise
    """
    try:
        with app.app_context():
            # Delete all rows from the database
            db.delete_all_rows()
        return jsonify({"message": "All rows deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
            csv_writer.writerow(
                ["id", "current_floor", "demand_floor", "destination_floor"]
            )

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
        return jsonify({"error": str(e)}), 500


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
    db.recreate_table()
    dg = DataGenerator()
    dg.generate(db)
    # Run the application on port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)
