import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import g4f

app = Flask(__name__)
CORS(app)

# जो प्रोवाइडर्स सबसे ज्यादा स्टेबल हैं और 'get_dict' एरर नहीं देते
PROVIDERS = [
    g4f.Provider.PollinationsAI,
    g4f.Provider.Pizzagpt,
    g4f.Provider.Airforce
]

@app.route("/")
def home():
    return jsonify({
        "status": "GPT4Free API Running",
        "mode": "Raw ChatCompletion Mode"
    })

@app.route("/test")
def test():
    results = []
    
    for provider in PROVIDERS:
        try:
            # बिना Client() के सीधे कोर g4f फ़ंक्शन का इस्तेमाल
            response = g4f.ChatCompletion.create(
                model="gpt-4o-mini",
                provider=provider,
                messages=[{"role": "user", "content": "Reply only with HI"}],
                stream=False
            )
            
            if response:
                results.append({
                    "provider": provider.__name__,
                    "status": "SUCCESS",
                    "reply": str(response)
                })
                return jsonify(results) # सफ़ल होते ही तुरंत रिस्पॉन्स भेजें

        except Exception as e:
            results.append({
                "provider": provider.__name__,
                "status": "FAILED",
                "error": str(e)
            })
            
    return jsonify(results)

@app.route("/scrape-ai", methods=["POST"])
def scrape_ai():
    try:
        data = request.get_json()
        if not data or "messages" not in data:
            return jsonify({"error": "Missing messages array"}), 400

        errors = []
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
                    
            except Exception as e:
                errors.append({
                    "provider": provider.__name__,
                    "error": str(e)
                })
                continue

        return jsonify({
            "error": "No provider worked",
            "details": errors
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
