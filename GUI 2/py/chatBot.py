from flask import Flask, request, jsonify
from chatBotFunctions import get_ml_response  # Import your ML model logic

app = Flask(__name__)

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data['message']
    
    # Pass the user's message to the ML model and get a response
    bot_response = get_ml_response(user_message)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
