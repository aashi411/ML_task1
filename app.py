from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)


# Pickle Class Fix
class DeliveryModel:
    def predict(self, distance, weight):
        return 0.5 + (distance * 0.2) + (weight * 0.1)


# Load model AFTER class definition
with open("delivery_model.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return "Delivery API Running"


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    distance = data["distance"]
    weight = data["weight"]

    prediction = model.predict(distance, weight)

    return jsonify({
        "distance": distance,
        "weight": weight,
        "estimated_delivery_time": prediction
    })


if __name__ == "__main__":
    app.run(debug=True)