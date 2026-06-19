import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import g4f

app = Flask(__name__)
CORS(app)

g4f.debug.logging = False

# Working providers
CONFIGS = [
    {
        "provider": g4f.Provider.PollinationsAI,
        "model": "openai"
    },
    {
        "provider": g4f.Provider.PuterJS,
        "model": "gpt-4o-mini"
    }
]


@app.route("/")
def home():
    return jsonify({
        "status": "GPT4Free API Running",
        "mode": "Live List Verified"
    })


@app.route("/test")
def test():
    results = []

    for cfg in CONFIGS:
        try:
            response = g4f.ChatCompletion.create(
                model=cfg["model"],
                provider=cfg["provider"],
                messages=[
                    {
                        "role": "user",
                        "content": "Reply only with HI"
                    }
                ]
            )

            if response:
                return jsonify({
                    "status": "SUCCESS",
                    "provider": cfg["provider"].__name__,
                    "reply": str(response)
                })

        except Exception as e:
            results.append({
                "provider": cfg["provider"].__name__,
                "status": "FAILED",
                "error": str(e)
            })

    return jsonify({
        "status": "FAILED",
        "details": results
    }), 500


@app.route("/scrape-ai", methods=["POST"])
def scrape_ai():
    try:
        data = request.get_json()

        if not data or "messages" not in data:
            return jsonify({
                "error": "Missing messages array"
            }), 400

        errors = []

        for cfg in CONFIGS:
            try:
                response = g4f.ChatCompletion.create(
                    model=cfg["model"],
                    provider=cfg["provider"],
                    messages=data["messages"]
                )

                if response:
                    return jsonify({
                        "provider": cfg["provider"].__name__,
                        "reply": str(response)
                    })

            except Exception as e:
                errors.append({
                    "provider": cfg["provider"].__name__,
                    "error": str(e)
                })

        return jsonify({
            "error": "No provider worked",
            "details": errors
        }), 500

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
