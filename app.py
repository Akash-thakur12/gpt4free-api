import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import g4f

app = Flask(__name__)
CORS(app)

g4f.debug.logging = False

# ये दोनों प्रोवाइडर्स बिना किसी API Key के बिल्कुल सही काम करते हैं
# इनके मॉडल नाम को नए सिंटैक्स के हिसाब से फिक्स कर दिया है
CONFIGS = [
    {"provider": g4f.Provider.PollinationsAI, "model": "gpt-4o"}, # Pollinations के लिए सही मॉडल नाम
    {"provider": g4f.Provider.DDG, "model": "gpt-4o-mini"}         # DuckDuckGo के लिए सही मॉडल नाम
]

@app.route("/")
def home():
    return jsonify({
        "status": "GPT4Free API Running",
        "mode": "Fixed Provider Catalog"
    })

@app.route("/test")
def test():
    results = []
    
    for cfg in CONFIGS:
        try:
            response = g4f.ChatCompletion.create(
                model=cfg["model"],
                provider=cfg["provider"],
                messages=[{"role": "user", "content": "Reply only with HI"}],
                stream=False
            )
            
            if response:
                return jsonify({
                    "status": "SUCCESS",
                    "provider": cfg["provider"].__name__,
                    "reply": str(response)
                }), 200

        except Exception as e:
            results.append({
                "provider": cfg["provider"].__name__,
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

        for cfg in CONFIGS:
            try:
                response = g4f.ChatCompletion.create(
                    model=cfg["model"],
                    provider=cfg["provider"],
                    messages=data["messages"],
                    stream=False
                )
                
                if response:
                    return jsonify({
                        "provider": cfg["provider"].__name__,
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
