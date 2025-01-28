from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Configure the Google AI API key
genai.configure(api_key="#Your Api key")

app = Flask(__name__)

# Prompt to guide the chatbot to respond with health-related information
HEALTH_PROMPT = """
You are a highly knowledgeable health assistant. Your role is to provide accurate, helpful, 
and reliable information only related to health, wellness, nutrition, medicine, mental health, 
and fitness. Do not respond to any query that is not related to health. give response in 2-3 lines
"""

def get_chatbot_response(user_input):
    
    """
    Generate a response from the chatbot.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{HEALTH_PROMPT}\nUser: {user_input}\nAssistant:")
    return response.text.strip()  # Return the text from the model

@app.route("/")
def index():
    """
    Serve the frontend HTML page (index.html).
    """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle chatbot queries from the frontend.
    """
    data = request.json  # Get the incoming data as JSON
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Get the response from the chatbot logic
    ai_response = get_chatbot_response(user_input)
    
    return jsonify({"response": ai_response})  # Return the chatbot's response in JSON format

if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask server
