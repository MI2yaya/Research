let loadedModel = null;

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

const selectedItem = getQueryParam('selectedItem');

// Function to preload model
function preloadModel() {
    if (selectedItem) {
        fetch('http://127.0.0.1:5000/api/preload-model', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ model: selectedItem }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                loadedModel = data.model;  // Store the loaded model's reference
                console.log(data.message);  // You can also update the UI to notify the user
                console.log(data.model);
            } else if (data.error) {
                console.error("Error preloading model:", data.error);
            }
        })
        .catch(error => console.error("Error:", error));
    }
}

// Function to send a message to the model
function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    if (userInput) {
        if (!loadedModel) {
            console.error("Model not loaded. Please preload the model first."); // If model not loaded
            return;
        }

        appendMessage('user', userInput);
        const fullChatHistory = generateChatHistory(); // generate after appending

        console.log(fullChatHistory);

        fetch('http://127.0.0.1:5000/api/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: fullChatHistory }),  
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                console.log("Bot response:", data.response);
                appendMessage('bot', data.response);  // Display the bot's response in your UI
            } else if (data.error) {
                console.error("Error processing message:", data.error);
            }
        })
        .catch(error => console.error("Error:", error));
    }
}

// Function to append a message to the UI
function appendMessage(sender, text) {
    let messageContainer = document.createElement('div');
    messageContainer.classList.add('message', `${sender}-message`);  // Corrected string interpolation
    messageContainer.textContent = `${sender.charAt(0).toUpperCase() + sender.slice(1)}: ${text}`;  // Corrected string interpolation
    document.getElementById('messages').appendChild(messageContainer);
}

// Function to generate chat history from UI
function generateChatHistory() {
    const messagesContainer = document.getElementById('messages');
    const messageElements = messagesContainer.getElementsByClassName('message');
    let chatHistory = "System: This is a conversation with a new therapist, do not refer to previous therapy sessions.\n";

    for (let messageElement of messageElements) {
        
        chatHistory += messageElement.textContent + "\n";
    }

    return chatHistory.trim();
}

window.onload = preloadModel; 
