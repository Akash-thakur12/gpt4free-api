import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from g4f.client import Client

app = Flask(__name__)
CORS(app)

client = Client()

@app.route("/")
def home():
    return jsonify({"status": "GPT4Free API Running", "mode": "Stealth"})

@app.route("/test")
def test():
    try:
        # यहाँ से हमने provider=g4f.Provider.Blackbox हटा दिया है
        # अब g4f खुद बैकएंड में चालू फ्री प्रोवाइडर ढूंढ लेगा
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Hello"}
            ]
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/scrape-ai", methods=["POST"])
def scrape_ai():
    try:
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({"error": "Missing messages array"}), 400

        # यहाँ भी ऑटोमैटिक बेस्ट प्रोवाइडर सिलेक्शन सेट कर दिया है
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=data["messages"]
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
