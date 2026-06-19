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
        # ऑटोमैटिक वर्किंग प्रोवाइडर को कॉल करना
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Hello"}
            ]
        )

        # स्ट्रक्चर को सुरक्षित पार्स करना
        reply_text = response.choices[0].message.content

        return jsonify({
            "reply": reply_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/scrape-ai", methods=["POST"])
def scrape_ai():
    try:
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({"error": "Missing messages array"}), 400

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=data["messages"]
        )

        reply_text = response.choices[0].message.content

        return jsonify({
            "reply": reply_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
