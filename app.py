import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from g4f.client import Client
import g4f.Provider

app = Flask(__name__)
CORS(app)

client = Client()

@app.route("/")
def home():
    return jsonify({
        "status": "GPT4Free API Running",
        "mode": "Forced Providers"
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

    providers = [
        g4f.Provider.DDGS,
        g4f.Provider.HuggingChat,
        g4f.Provider.You,
        g4f.Provider.PollinationsAI
    ]

    for provider in providers:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                provider=provider,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello"
                    }
                ]
            )

            return jsonify({
                "provider": provider.__name__,
                "reply": response.choices[0].message.content
            })

        except Exception as e:
            print(f"{provider.__name__} failed: {e}")
            continue

    return jsonify({
        "error": "No provider worked"
    }), 500


@app.route("/scrape-ai", methods=["POST"])
def scrape_ai():

    try:
        data = request.get_json()

        if not data or "messages" not in data:
            return jsonify({
                "error": "Missing messages array"
            }), 400

        providers = [
            g4f.Provider.DDGS,
            g4f.Provider.HuggingChat,
            g4f.Provider.You,
            g4f.Provider.PollinationsAI
        ]

        for provider in providers:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    provider=provider,
                    messages=data["messages"]
                )

                return jsonify({
                    "provider": provider.__name__,
                    "reply": response.choices[0].message.content
                })

            except Exception as provider_error:
                print(f"{provider.__name__} failed: {provider_error}")
                continue

        return jsonify({
            "error": "No provider worked"
        }), 500

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
