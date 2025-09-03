from flask import Flask, request, jsonify
import os
import re
import json
from google import genai
from flask_cors import CORS
CORS(app)

app = Flask(__name__)

# API key environment variable se aayegi
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def clean_json_output(raw_text: str):
    """
    Cleans Gemini output and ensures valid JSON is returned.
    """
    # Remove code fences like ```json ... ```
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
    
    try:
        return json.loads(cleaned)  # Try parsing JSON
    except Exception:
        # If parsing fails, return raw string for debugging
        return {"error": "Invalid JSON", "raw_output": raw_text}
    
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        user_input = data.get("prompt", "")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )
        cleaned_response = clean_json_output(response.text)

        return jsonify(cleaned_response)
        # try:
        #     parsed = json.loads(response.text)
        #     return jsonify(parsed)
        # except Exception:
        #     return jsonify({"error": "Invalid JSON response", "raw": response.text})

    except Exception as e:
        return jsonify({"error": str(e)})