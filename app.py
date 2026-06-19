import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import g4f

app = Flask(__name__)
CORS(app)

# कुकीज़ और इंटरनल लॉगिंग एरर से बचने के लिए इसे बंद रखें
g4f.debug.logging = False

# नए अपडेट के अनुसार सही नाम (ApiAirforce) इस्तेमाल किया गया है
PROVIDERS = [
    g4f.Provider.ApiAirforce,
    g4f.Provider.PollinationsAI
]

@app.route("/")
def home():
    return jsonify({
        "status": "GPT4Free API Running",
        "mode": "Stealth Providers Locked"
    })

@app.route("/test")
def test():
    results = []
    
    for provider in PROVIDERS:
        try:
            # बिना कुकीज़ वाले डायरेक्ट प्रोवाइडर को कॉल करना
            response = g4f.ChatCompletion.create(
                model="gpt-4o-mini",
                provider=provider,
                messages=[{"role": "user", "content": "Reply only with HI"}],
                stream=False
            )
            
            if response:
                return jsonify({
                    "status": "SUCCESS",
                    "provider": provider.__name__,
                    "reply": str(response)
                }), 200

        except Exception as e:
            results.append({
                "provider": provider.__name__,
                "status": "FAILED",
                "error": str(e)
            })
            continue
            
    return jsonify({
        "status": "FAILED",
        "details": results
    }), 500

@app.route("/scrape-ai", methods=["POST"])
def scrape_ai():
    try:
        data = request.get_json()
        if not data or "messages" not in data:
            return jsonify({"error": "Missing messages array"}), 400

        for provider in PROVIDERS:
            try:
                response = g4f.ChatCompletion.create(
                    model="gpt-4o-mini",
                    provider=provider,
                    messages=data["messages"],
                    stream=False
                )
                
                if response:
                    return jsonify({
                        "provider": provider.__name__,
                        "reply": str(response)
                    }), 200
            except Exception:
                continue

        return jsonify({"error": "पंडित जी अभी ध्यान में हैं, कृपया दोबारा प्रयास करें।"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
