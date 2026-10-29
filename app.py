import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:5000"
)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/data")
def save_data():
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/data",
            json=request.get_json(),
            timeout=5
        )

        return (
            response.content,
            response.status_code,
            {"Content-Type": "application/json"}
        )

    except requests.RequestException:
        return jsonify({
            "error": "Backend недоступен"
        }), 502


@app.get("/api/data")
def get_data():
    try:
        params = {}

        if request.args.get("limit"):
            params["limit"] = request.args["limit"]

        response = requests.get(
            f"{BACKEND_URL}/api/data",
            params=params,
            timeout=5
        )

        return (
            response.content,
            response.status_code,
            {"Content-Type": "application/json"}
        )

    except requests.RequestException:
        return jsonify({
            "error": "Backend недоступен"
        }), 502


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )