from flask import Flask, request, jsonify
import g4f

app = Flask(__name__)

@app.route("/")
def home():
    return "GPT4Free API Running"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt")

    response = g4f.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return jsonify({
        "answer": str(response)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
