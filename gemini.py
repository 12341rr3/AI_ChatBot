from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import urllib.parse
app = Flask(__name__)
CORS(app)  # allow frontend access

# 🔐 Set your API key (use environment variable ideally)
genai.configure(api_key="AIzaSyAQM97tp2ypGK1mcggZ6DsteN0Qp2BKOaA")

model = genai.GenerativeModel("gemini-2.5-flash")


# ===============================
# 🧠 TEXT RESPONSE API
# ===============================
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        contents = data.get("contents", [])

        # ✅ Extract text properly
        user_text = ""
        for item in contents:
            for part in item.get("parts", []):
                if "text" in part:
                    user_text += part["text"] + "\n"

        print("🟢 USER:", user_text)

        # ✅ Correct Gemini call
        response = model.generate_content(user_text)

        print("🟢 GEMINI:", response.text)

        return jsonify({
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": response.text
                    }]
                }
            }]
        })

    except Exception as e:
        print("❌ BACKEND ERROR:", e)
        return jsonify({"error": str(e)}), 500
# ===============================
# 🎨 IMAGE GENERATION API
# ===============================
@app.route("/ask-image", methods=["POST"])
def ask_image():
    try:
        data = request.json
        prompt = data.get("prompt")

        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt)

        # 🔥 More reliable endpoint
        image_url = f"https://pollinations.ai/p/{encoded_prompt}"

        return jsonify({
            "success": True,
            "image": image_url
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

# ===============================
# 🚀 RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)