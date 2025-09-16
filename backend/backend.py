from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
	
# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tasks = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")

    # Send message to OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # lightweight & fast
        messages=[
            {"role": "system", "content": "You are a helpful AI To-Do assistant. Help manage tasks: add, list, complete, delete. Keep responses short and clear."},
            {"role": "user", "content": msg}
        ]
    )
    reply = completion.choices[0].message.content

    # Simple keyword-based task updates
    msg_lower = msg.lower()
    if "add" in msg_lower:
        task = msg_lower.replace("add", "").replace("task", "").strip()
        if task:
            tasks.append(task)
    elif "list" in msg_lower:
        pass
    elif "done" in msg_lower or "complete" in msg_lower:
        for t in tasks:
            if t in msg_lower:
                tasks.remove(t)
                break
    elif "delete" in msg_lower:
        for t in tasks:
            if t in msg_lower:
                tasks.remove(t)
                break

    return jsonify({"reply": reply, "tasks": tasks})

if __name__ == "__main__":
    app.run(debug=True)
    return jsonify({"reply": reply, "tasks": tasks})
	

if __name__ == "__main__":
    app.run(debug=True)
