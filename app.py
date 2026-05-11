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
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Delivery Time Predictor</title>

        <style>
            *{
                margin:0;
                padding:0;
                box-sizing:border-box;
                font-family:Arial, sans-serif;
            }

            body{
                height:100vh;
                display:flex;
                justify-content:center;
                align-items:center;
                background:linear-gradient(135deg,#141e30,#243b55);
                color:white;
            }

            .container{
                width:420px;
                padding:35px;
                border-radius:18px;
                background:rgba(255,255,255,0.08);
                backdrop-filter:blur(10px);
                box-shadow:0 8px 25px rgba(0,0,0,0.3);
                text-align:center;
            }

            h1{
                font-size:32px;
                margin-bottom:10px;
            }

            p{
                color:#dcdcdc;
                margin-bottom:25px;
                line-height:1.5;
            }

            .endpoint{
                background:#111827;
                padding:15px;
                border-radius:10px;
                margin-bottom:20px;
                font-family:monospace;
                font-size:16px;
                border:1px solid rgba(255,255,255,0.1);
            }

            .status{
                display:inline-block;
                padding:10px 18px;
                border-radius:30px;
                background:#22c55e;
                color:white;
                font-weight:bold;
                font-size:14px;
            }

            .footer{
                margin-top:20px;
                font-size:13px;
                color:#bbbbbb;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>Delivery Predictor</h1>

            <p>
                Flask API that predicts delivery time
                using package distance and weight.
            </p>

            <div class="endpoint">
                POST /predict
            </div>

            <div class="status">
                API LIVE
            </div>

            <div class="footer">
                Powered by Flask + Pickle
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