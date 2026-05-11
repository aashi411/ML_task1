from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)


# Pickle Class Fix
class DeliveryModel:
    def predict(self, distance, weight):
        return 0.5 + (distance * 0.2) + (weight * 0.1)


with open("delivery_model.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Delivery Time Predictor</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .container {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                text-align: center;
                width: 350px;
            }

            h1 {
                color: #333;
                margin-bottom: 10px;
            }

            p {
                color: #666;
            }

            .endpoint {
                margin-top: 20px;
                background: #f0f0f0;
                padding: 10px;
                border-radius: 8px;
                font-family: monospace;
            }

            .status {
                margin-top: 15px;
                color: green;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Delivery Time Predictor</h1>
            <p>Flask API for estimating delivery time based on distance and weight.</p>

            <div class="endpoint">
                POST /predict
            </div>

            <div class="status">
                API Running Successfully
            </div>
        </div>

    </body>
    </html>
    """


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