from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from forecast_model import run_forecast
from generate_tips import run_tips

app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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


@app.route("/csv-files", methods=["GET"])
def list_files():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".csv")]
    return jsonify(files)


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


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

@app.route("/run-tips", methods=["POST"])
def run_tips():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    csv_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(csv_path):
        return jsonify({"error": "File does not exist"}), 400

    from generate_tips import run_tips
    result = run_tips(csv_path)
    return jsonify(result)

@app.route("/tips_plot.png")
def tips_plot():
    forecast_dir = os.path.join(os.path.dirname(__file__), "forecast")
    return send_from_directory(forecast_dir, "tips_tree.png")




if __name__ == "__main__":
    app.run(debug=True, port=5000)
