import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import g4f

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "status": "GPT4Free API Running",
        "mode": "Pure Auto-Fallback Mode"
    })

@app.route("/test")
def test():
    try:
        # बिना किसी प्रोवाइडर को फोर्स किए सीधे कोर फंक्शन का इस्तेमाल
        # g4f खुद लाइव प्रोवाइडर (जैसे Pollinations, Airforce, DDG) ढूंढ लेगा
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply only with HI"}],
            stream=False
        )
        
        if response:
            return jsonify({
                "status": "SUCCESS",
                "reply": str(response)
            }), 200
        else:
            return jsonify({"status": "FAILED", "error": "Empty response"}), 500

    except Exception as e:
        return jsonify({
            "status": "FAILED",
            "error": str(e)
        }), 500

@app.route("/scrape-ai", methods=["POST"])
def scrape_ai():
    try:
        data = request.get_json()
        if not data or "messages" not in data:
            return jsonify({"error": "Missing messages array"}), 400

        # मुख्य चैट एंडपॉइंट के लिए भी ऑटोमैटिक बेस्ट प्रोवाइडर सिलेक्शन
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=data["messages"],
            stream=False
        )
        
        if response:
            return jsonify({
                "reply": str(response)
            }), 200
        else:
            return jsonify({"error": "No response from working providers"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
