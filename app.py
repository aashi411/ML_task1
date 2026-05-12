from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import pickle
import os
import sys

app = Flask(__name__)

# Enable CORS
CORS(app)

# -----------------------------
# MODEL DEFINITION
# -----------------------------
# This class MUST match train.py
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


# -----------------------------
# CUSTOM UNPICKLER FIX
# -----------------------------
# Fixes Render/Gunicorn pickle issue
class ModelUnpickler(pickle.Unpickler):

    def find_class(self, module, name):

        if name == "DeliveryModel":
            return DeliveryModel

        return super().find_class(module, name)


# -----------------------------
# RATE LIMITER
# -----------------------------
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "30 per hour"],
    storage_uri="memory://",
)

# -----------------------------
# LOAD MODEL
# -----------------------------
model = None

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "delivery_model.pkl"
)

try:

    if os.path.exists(MODEL_PATH):

        with open(MODEL_PATH, "rb") as file:
            model = ModelUnpickler(file).load()

        print("Model loaded successfully")

    else:
        print("delivery_model.pkl not found")

except Exception as e:
    print(f"Error loading model: {e}")


# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/")
@limiter.exempt
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
                font-family:Arial,sans-serif;
            }

            body{
                height:100vh;
                display:flex;
                justify-content:center;
                align-items:center;
                background:linear-gradient(135deg,#141e30,#243b55);
                color:white;
            }

            .card{
                width:420px;
                padding:40px;
                border-radius:20px;
                background:rgba(255,255,255,0.08);
                backdrop-filter:blur(12px);
                box-shadow:0 8px 25px rgba(0,0,0,0.3);
                text-align:center;
            }

            h1{
                margin-bottom:12px;
                font-size:32px;
            }

            p{
                color:#d1d5db;
                line-height:1.6;
                margin-bottom:20px;
            }

            .endpoint{
                background:#111827;
                padding:14px;
                border-radius:10px;
                margin-bottom:20px;
                font-family:monospace;
            }

            .status{
                display:inline-block;
                padding:10px 18px;
                border-radius:30px;
                background:#22c55e;
                font-weight:bold;
            }

        </style>

    </head>

    <body>

        <div class="card">

            <h1>Delivery Predictor</h1>

            <p>
                Flask API for estimating delivery time
                based on customer distance and package weight.
            </p>

            <div class="endpoint">
                POST /predict
            </div>

            <div class="status">
                API LIVE
            </div>

        </div>

    </body>

    </html>
    """


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.route("/health", methods=["GET"])
def health_check():

    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "python_version": sys.version
    })


# -----------------------------
# PREDICTION ROUTE
# -----------------------------
@app.route("/predict", methods=["POST"])
@limiter.limit("10 per minute")
def predict():

    if model is None:
        return jsonify({
            "error": "Model not available"
        }), 500

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400

        distance = float(data.get("distance", 0))
        weight = float(data.get("weight", 0))

        # Validation
        if distance < 0 or weight < 0:

            return jsonify({
                "error": "Values cannot be negative"
            }), 400

        prediction = model.predict(
            distance,
            weight
        )

        return jsonify({

            "status": "success",

            "distance": distance,

            "weight": weight,

            "estimated_delivery_time": round(
                prediction,
                2
            ),

            "unit": "hours"

        })

    except (ValueError, TypeError):

        return jsonify({
            "error": "Invalid input format"
        }), 400

    except Exception as e:

        return jsonify({
            "error": "Internal server error"
        }), 500


# -----------------------------
# RATE LIMIT ERROR
# -----------------------------
@app.errorhandler(429)
def ratelimit_handler(e):

    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Too many requests"
    }), 429


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )