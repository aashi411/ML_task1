import pickle


class DeliveryModel:
    def predict(self, distance, weight):
        return 0.5 + (distance * 0.2) + (weight * 0.1)


model = DeliveryModel()

with open("delivery_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved as delivery_model.pkl")