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
