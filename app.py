
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from g4f.client import Client
import g4f.Provider

app = Flask(__name__)
CORS(app)

client = Client()

# Stable providers
PROVIDERS = [
    g4f.Provider.PollinationsAI
]

@app.route("/")
def home():
    return jsonify({
        "status": "GPT4Free API Running"
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
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/test")
def test():

    results = []

    for provider in PROVIDERS:

        try:

            response = client.chat.completions.create(
                model="default",
                provider=provider,
                messages=[
                    {
                        "role": "user",
                        "content": "Reply only with HI"
                    }
                ]
            )

            reply = response.choices[0].message.content

            results.append({
                "provider": provider.__name__,
                "status": "SUCCESS",
                "reply": reply
            })

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
            return jsonify({
                "error": "Missing messages array"
            }), 400

        errors = []

        for provider in PROVIDERS:

            try:

                response = client.chat.completions.create(
                    model="default",
                    provider=provider,
                    messages=data["messages"]
                )

                reply = response.choices[0].message.content

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

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

