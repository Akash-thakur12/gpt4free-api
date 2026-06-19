import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import g4f

app = Flask(__name__)
CORS(app)

# कुकीज़ और लॉगिंग एरर से बचने के लिए इसे डिसेबल करें
g4f.debug.logging = False

# केवल वे प्रोवाइडर्स जो बिना कुकीज़/फ़ाइल सिस्टम के सीधे चलते हैं
STABLE_PROVIDER = g4f.Provider.Airforce  # या g4f.Provider.PollinationsAI

@app.route("/")
def home():
    return jsonify({
        "status": "GPT4Free API Running",
        "mode": "No-Cookies API Mode"
    })

@app.route("/test")
def test():
    try:
        # यहाँ हम सीधे स्टेबल प्रोवाइडर फ़ोर्स कर रहे हैं जो कुकीज़ नहीं मांगता
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            provider=STABLE_PROVIDER,
            messages=[{"role": "user", "content": "Reply only with HI"}],
            stream=False
        )
        
        if response:
            return jsonify({
                "status": "SUCCESS",
                "provider": STABLE_PROVIDER.__name__,
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

        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            provider=STABLE_PROVIDER,
            messages=data["messages"],
            stream=False
        )
        
        if response:
            return jsonify({
                "reply": str(response)
            }), 200
        else:
            return jsonify({"error": "No response from working provider"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
