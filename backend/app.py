from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from forecast_model import run_forecast
from generate_tips import run_tips as generate_tips_func
from co2_tracker import generate_co2_plot

# Serve React build folder
app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
CORS(app)

# Folder where uploaded CSVs will be stored
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------
# FILE UPLOAD
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully!"})


# ---------------------------
# LIST CSV FILES
# ---------------------------
@app.route("/csv-files", methods=["GET"])
def list_files():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".csv")]
    return jsonify(files)


# ---------------------------
# FORECAST API
# ---------------------------
@app.route("/run-forecast", methods=["POST"])
def run_forecast_api():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    csv_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(csv_path):
        return jsonify({"error": "File does not exist"}), 400

    result = run_forecast(csv_path)
    return jsonify(result)


@app.route("/forecast_plot.png")
def serve_plot():
    forecast_dir = os.path.join(os.path.dirname(__file__), "forecast")
    return send_from_directory(forecast_dir, "forecast_plot.png")


# ---------------------------
# ENERGY SAVING TIPS
# ---------------------------
@app.route("/run-tips", methods=["POST"])
def run_tips_api():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    csv_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(csv_path):
        return jsonify({"error": "File does not exist"}), 400

    result = generate_tips_func(csv_path)
    return jsonify(result)


@app.route("/tips_plot.png")
def tips_plot():
    forecast_dir = os.path.join(os.path.dirname(__file__), "forecast")
    return send_from_directory(forecast_dir, "tips_tree.png")


# ---------------------------
# CO₂ LINEAR REGRESSION PLOT
# ---------------------------
@app.route("/co2-plot", methods=["POST"])
def co2_plot_api():
    data = request.json
    filename = data.get("filename")

    try:
        output = generate_co2_plot(filename)
        return jsonify({
            "status": "success",
            "image": output
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/co2_plot.png")
def serve_co2_plot():
    forecast_dir = os.path.join(os.path.dirname(__file__), "forecast")
    return send_from_directory(forecast_dir, "co2_plot.png")


# ---------------------------
# ABOUT (STATIC DATA FOR FRONTEND)
# ---------------------------
@app.route("/about-info", methods=["GET"])
def about_info():
    return jsonify({
        "appName": "SmartAI Energy Saver",
        "version": "1.0",
        "description": "SmartAI Energy Saver analyzes electricity usage, predicts future consumption, calculates CO₂ impact, and offers personalized energy-saving recommendations using machine learning and data analytics.",
        "features": [
            "Electricity Bill Forecasting",
            "CO₂ Emission Tracking & Trends",
            "Smart Energy-Saving Tips",
            "Bill Upload & Auto-Cleaning",
            "Interactive Charts & Visuals"
        ]
    })


# ---------------------------
# SERVE REACT FRONTEND
# ---------------------------
@app.route("/", defaults={"path": ""})
@app.route("/about")
def serve_react(path):
    full_path = os.path.join(app.static_folder, path)

    if path != "" and os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)

    return send_from_directory(app.static_folder, "index.html")


# ---------------------------
# START SERVER
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
