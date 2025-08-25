from flask import Flask, request, jsonify
import os
from google import genai

app = Flask(__name__)

# API key environment variable se aayegi
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        user_input = data.get("prompt", "")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )

        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})
