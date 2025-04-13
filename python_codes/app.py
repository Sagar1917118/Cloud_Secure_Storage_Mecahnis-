from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 Import this
from IDA import InformationDispersalAlgorithm
import numpy as np
import base64
app = Flask(__name__)
CORS(app)  # 👈 Enable CORS for all routes and origins

# Initialize with your desired m and n
ida = InformationDispersalAlgorithm(m=3, n=5)

@app.route("/encode", methods=["POST"])
def encode():
    try:
        text = request.json.get("text")
        if not text:
            return jsonify({"error": "Missing text"}), 400
        decoded_text = base64.b64decode(text).decode('utf-8')
        encoded = ida.disperse(decoded_text)
        return jsonify({
            "encoded_fragments": encoded.tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/decode", methods=["POST"])
def decode():
    try:
        fragments = request.json.get("fragments")
        if fragments is None:
            return jsonify({"error": "Missing fragments or indices"}), 400

        fragments = np.array(fragments, dtype=int)
        result = ida.reconstruct(fragments)

        return jsonify({"recovered": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")
