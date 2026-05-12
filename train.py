import pickle


class DeliveryModel:

    def __init__(self):
        self.base_time = 0.5
        self.distance_coeff = 0.2
        self.weight_coeff = 0.1

    def predict(self, distance, weight):
        return (
            self.base_time
            + (distance * self.distance_coeff)
            + (weight * self.weight_coeff)
        )


model = DeliveryModel()

with open("delivery_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("delivery_model.pkl created successfully")