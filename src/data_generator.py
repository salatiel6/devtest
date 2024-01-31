import os
import json


class DataGenerator:
    @staticmethod
    def generate(db):
        # Obtém o diretório do script atual
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Constrói o caminho completo para o arquivo JSON
        json_path = os.path.join(script_dir, 'elevator_travels.json')

        # Verifica se o arquivo existe antes de tentar abri-lo
        if os.path.exists(json_path):
            # Carrega os dados do arquivo JSON
            with open(json_path, 'r') as file:
                data = json.load(file)

            # Itera sobre os dados e insere no banco de dados
            for travel in data:
                current_floor = travel['current_floor']
                demand_floor = travel['demand_floor']
                destination_floor = travel['destination_floor']

                db.insert_call(current_floor, demand_floor, destination_floor)
        else:
            print(f"Arquivo não encontrado: {json_path}")
