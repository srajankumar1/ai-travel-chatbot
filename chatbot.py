from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GROQ_API_KEY")

# Groq Client
client = Groq(api_key=api_key)

# Chat History
messages = [
    {
        "role": "system",
        "content": """
You are an intelligent travel guide chatbot.

Your responsibilities:
- Suggest tourist places
- Create budget-friendly travel plans
- Recommend hotels
- Give travel tips
- Suggest food and local attractions

Keep responses short and friendly.
"""
    }
]

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Chat API
@app.route("/chat", methods=["POST"])
def chat():

    user_input = request.json["message"]

    # Store user message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # AI Response
    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=messages
    )

    reply = completion.choices[0].message.content

    # Store assistant reply
    messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    return jsonify(
        {
            "reply": reply
        }
    )

# Run App
if __name__ == "__main__":
    app.run(debug=True)