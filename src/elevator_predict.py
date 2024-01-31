class DynamicElevatorPredictor:
    def __init__(self, forgetting_factor=0.25):
        self.demand_counts = {}
        self.resting_floor = None
        self.forgetting_factor = forgetting_factor

    def train(self, data):
        for entry in data:
            if entry['action'] == 'call':
                floor = entry['floor']
                self.demand_counts[floor] = self.demand_counts.get(floor, 0) + 1

        self.update_resting_floor()

        print(f"Demand counts train: {self.demand_counts}")
        print(f"Trained Resting Floor: {self.resting_floor}")

    def update_resting_floor(self):
        # Escolhendo o resting floor como o andar com a maior demanda
        self.resting_floor = max(self.demand_counts, key=self.demand_counts.get)

    def predict_resting_floor(self, new_calls):
        # Esquecendo observações antigas
        for floor, count in list(self.demand_counts.items()):
            self.demand_counts[floor] = count * self.forgetting_factor

        print(f"Demand counts forg: {self.demand_counts}")

        # Atualizando a contagem de demandas com base nas novas chamadas
        for floor in new_calls:
            self.demand_counts[floor] = self.demand_counts.get(floor, 0) + 1

        print(f"Demand counts new: {self.demand_counts}")

        self.update_resting_floor()

        print(f"Predicted Resting Floor: {self.resting_floor}")

        return self.resting_floor

# Exemplo de uso:
dynamic_elevator_predictor = DynamicElevatorPredictor()

# Histórico de demanda (use seu próprio histórico)
demand_history = [
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 2, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 3, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 4, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 5, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    {'floor': 6, 'action': 'call'},
    {'floor': 1, 'action': 'call'},
    # ...
]

# Treinando o modelo com base no histórico de demanda
dynamic_elevator_predictor.train(demand_history)

# Chamadas recentes para prever o próximo resting_floor
new_calls = [3, 2, 4, 2, 5, 2, 6, 2, 3, 2, 4, 2, 5, 2, 6, 2, 3, 2, 4, 2, 5, 2, 6, 2, ]

# Fazendo a previsão
predicted_resting_floor = dynamic_elevator_predictor.predict_resting_floor(new_calls)
