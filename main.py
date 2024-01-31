import csv

from src import db, Elevator, DataGenerator
from flask import Flask, jsonify, request, make_response
from io import StringIO

elevator = Elevator()
app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})


@app.route('/generate-data', methods=['GET'])
def generate_data():
    try:
        with app.app_context():
            db.recreate_table()
            data_generator = DataGenerator()
            data_generator.generate()

        return jsonify({'message': 'Data generated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/call-elevator', methods=['POST'])
def call_elevator():
    try:
        data = request.get_json()
        demand_floor = data['demand_floor']
        destination_floor = data['destination_floor']

        with app.app_context():
            elevator.call_elevator(demand_floor, destination_floor)

        return jsonify({'message': 'Elevator called successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get-all-rows', methods=['GET'])
def get_all_rows():
    try:
        with app.app_context():
            rows = db.get_all_rows()

            result = [{
                'id': row[0],
                'current_floor': row[1],
                'demand_floor': row[2],
                'destination_floor': row[3]
            } for row in rows]

            return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update-row', methods=['PUT'])
def update_row():
    try:
        data = request.get_json()

        if 'id' in data:
            row_id = data['id']

            if 'current_floor' in data:
                db.update_current_floor(row_id, data['current_floor'])

            if 'demand_floor' in data:
                db.update_demand_floor(row_id, data['demand_floor'])

            if 'destination_floor' in data:
                db.update_destination_floor(row_id, data['destination_floor'])

            return jsonify({'message': f'Row {row_id} updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete-all-rows', methods=['DELETE'])
def delete_all_rows():
    try:
        with app.app_context():
            db.delete_all_rows()
        return jsonify({'message': 'All rows deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/export-csv', methods=['GET'])
def export_csv():
    try:
        with app.app_context():
            rows = db.get_all_rows()
            csv_data = StringIO()
            csv_writer = csv.writer(csv_data)

            # Escreve o cabeçalho
            csv_writer.writerow(['id', 'current_floor', 'demand_floor', 'destination_floor'])

            # Escreve os dados
            csv_writer.writerows(rows)

            csv_data.seek(0)

        response = make_response(csv_data.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=elevator_data.csv'
        response.headers['Content-Type'] = 'text/csv'

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
