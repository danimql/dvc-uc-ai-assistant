from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env from repo root
ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# Import your backend logic
from src.ai_agent import run_my_logic

app = Flask(__name__)
CORS(app)

@app.route("/api/run", methods=["POST"])
def run_api():
    try:
        data = request.get_json(force=True) or {}
        prompt = (data.get("prompt") or "").strip()
        if not prompt:
            return jsonify({"error": "Missing 'prompt'"}), 400

        result = run_my_logic(prompt)
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
