#dont forget to run this

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
from py.chatBotFunctions import load_ml_model, get_ml_response
import traceback
import os

app = Flask(__name__)

CORS(app)

# Global variable to store the loaded model
loaded_model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatBot')
def chatBot():
    return render_template('chatBot.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route to preload the model
@app.route('/api/preload-model', methods=['POST'])
def preload_model():
    global loaded_model
    try:
        data = request.get_json()
        character = data['character']
        model = data['model']
        
        # Load the model and store it in the global variable
        loaded_model = load_ml_model(character,model)
        return jsonify({
            "message": f"Model {loaded_model} preloaded successfully",
            "model": loaded_model
            })
    except Exception as e:
        # Capture and log the exception
        error_message = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error preloading model: {error_message}\n{traceback_str}")
        return jsonify({"error": f"Failed to preload model: {error_message}"}), 500

# Route to send messages
@app.route('/api/send-message', methods=['POST'])
def send_message():
    global loaded_model
    try:
        data = request.get_json()
        user_message = data['message']

        print("waiting..")
        print(user_message)
         
        # Check if a model has been loaded
        if not loaded_model:
            raise ValueError("Model not loaded. Please preload a model first.")

        # Pass the user's message to the loaded ML model and get a response
        bot_response = get_ml_response(user_message)
        print(bot_response)
        if bot_response[:4].lower()=="bot:":
            bot_response=bot_response[4:]
        print("its alive ",bot_response)
        return jsonify({"response": bot_response})
    except Exception as e:
        # Capture and log the exception
        error_message = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error processing message: {error_message}\n{traceback_str}")
        return jsonify({"error": f"Failed to process message: {error_message}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT from environment or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
