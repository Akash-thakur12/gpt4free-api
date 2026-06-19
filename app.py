import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from g4f.client import Client
import g4f.Provider

app = Flask(__name__)
CORS(app)

client = Client()

# सबसे स्टेबल और हमेशा काम करने वाले प्रोवाइडर्स का पूल
PROVIDERS = [
    g4f.Provider.PollinationsAI,  # अब यह सही मॉडल के साथ काम करेगा
    g4f.Provider.DDG,             # DuckDuckGo बैकअप
    g4f.Provider.Pizzagpt         # PizzaGPT बैकअप
]

@app.route("/")
def home():
    return jsonify({
        "status": "GPT4Free API Running",
        "mode": "Stealth Fixed"
    })


@app.route("/providers")
def providers():
    try:
        provider_list = [
            name for name in dir(g4f.Provider)
            if not name.startswith("_")
        ]
        return jsonify({
            "providers": provider_list
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/test")
def test():
    results = []

    for provider in PROVIDERS:
        try:
            # यहाँ model को "default" से बदलकर "gpt-4o-mini" कर दिया है
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                provider=provider,
                messages=[
                    {
                        "role": "user",
                        "content": "Reply only with HI"
                    }
                ]
            )

            # नए g4f स्ट्रक्चर के अनुसार सीधे ऑब्जेक्ट एक्सेस करना
            reply = response.choices.message.content

            results.append({
                "provider": provider.__name__,
                "status": "SUCCESS",
                "reply": reply
            })
            return jsonify(results) # अगर पहला ही पास हो जाए तो तुरंत रिटर्न करें

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
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # यहाँ भी मॉडल फिक्स कर दिया है
                    provider=provider,
                    messages=data["messages"]
                )

                reply = response.choices.message.content

                if reply:
                    return jsonify({
                        "provider": provider.__name__,
                        "reply": reply
                    })

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
