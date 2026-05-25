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

# Chat History with Added Domain Constraints
messages = [
    {
        "role": "system",
        "content": 
        """
You are an intelligent travel guide chatbot.

Your responsibilities:
• Suggest tourist places
• Create budget-friendly travel plans
• Recommend hotels
• Give travel tips
• Suggest food and local attractions

DOMAIN CONSTRAINTS :
• You must ONLY answer questions related to travel, tourism, itineraries, geography, accommodation, and local culture.
• If the user asks about anything outside of travel (e.g., programming, mathematics, general science, politics, cooking recipes, or life advice), you must politely decline to answer.
• Standard Refusal Response: "I am sorry, but I can only assist you with travel-related queries! 🌍✈️"

IMPORTANT FORMATTING:
- Always give responses in pointwise format.
- Use numbering like:
  1. Place name
  2. Place name
- Keep answers short and clean.
- Add emojis where suitable.
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
