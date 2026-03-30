from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import urllib.parse
app = Flask(__name__)
CORS(app)  # allow frontend access

# 🔐 Set your API key (use environment variable ideally)
genai.configure(api_key="AIzaSyDo0cJc5a82PN9KWubajx7QwPGjezC9Uew")

model = genai.GenerativeModel("gemini-2.5-flash")


# ===============================
# 🧠 TEXT RESPONSE API
# 
#===============================

@app.route("/ask", methods=["POST"])

def ask():
    print("🔥 API HIT")
    try:
        data = request.json
        contents = data.get("contents", [])

        print("🟢 REQUEST:", contents)

        response = model.generate_content(contents)

        ai_text = response.text if hasattr(response, "text") else "No response"

        print("🟢 GEMINI:", ai_text)

        return jsonify({
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": ai_text
                    }]
                }
            }]
        })

    except Exception as e:
        print("❌ BACKEND ERROR:", e)
        return jsonify({"error": str(e)}), 500
# ===============================

# ===============================
# 🚀 RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
