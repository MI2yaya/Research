let loadedModel = null;
let debounceTimeout = null;

const BASE_URL = window.location.hostname === '127.0.0.1' ? 'http://127.0.0.1:5000' : 'https://ai-psychotherapy-training-deployment.onrender.com';

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

const selectedItem = getQueryParam('selectedItem');
const selectedModel = getQueryParam('selectedModel')
// Function to preload model
function preloadModel() {
    if (selectedItem && selectedModel) {
        fetch(`${BASE_URL}/api/preload-model`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                character: selectedItem,
                model: selectedModel
            }),
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
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
        let userInput = document.getElementById('user-input').value;
        if (userInput) {
            if (!loadedModel) {
                console.error("Model not loaded. Please preload the model first."); // If model not loaded
                return;
            }
            
            var inputField = document.getElementById("user-input");
            var sendButton = document.getElementById("send-button");
            

            inputField.disabled = true;
            sendButton.disabled = true;

            appendMessage('Therapist', userInput);
            const fullChatHistory = generateChatHistory(); // dont include . . .
            appendMessage('Patient',". . .",true);

            document.getElementById('user-input').value = '';

            console.log(fullChatHistory);

            fetch(`${BASE_URL}/api/send-message`, {
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
                    appendMessage('Patient', data.response);  // Display the bot's response in your UI

                    inputField.disabled = false;
                    sendButton.disabled = false;

                    document.getElementById("filler")?.remove(); 

                } else if (data.error) {
                    console.error("Error processing message:", data.error);

                    inputField.disabled = false;
                    sendButton.disabled = false;

                    document.getElementById("filler")?.remove(); 
                }
            })
            .catch(error => {
                console.error("Error:", error);
                inputField.disabled = false;
                sendButton.disabled = false;

                document.getElementById("filler")?.remove(); 
            });
        }
    }, 300);
}

// Function to append a message to the UI
function appendMessage(sender, text, filler=false) {
    const messageContainer = document.createElement('div');
    const chatContainer = document.getElementById('chatbox')
    if(filler){
        messageContainer.classList.add('message', `${sender}-message`,"filler")
        messageContainer.id="filler"
    }else{
        messageContainer.classList.add('message', `${sender}-message`);
    }
    messageContainer.textContent = `${sender.charAt(0).toUpperCase() + sender.slice(1)}: ${text}`;

    document.getElementById('messages').appendChild(messageContainer);

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Function to generate chat history from UI
function generateChatHistory() {
    const messagesContainer = document.getElementById('messages');
    const messageElements = messagesContainer.getElementsByClassName('message');
    let chatHistory = "System: This is a conversation with a new therapist, who you have not talked with prior, do not refer to prior sessions.\n";

    for (let messageElement of messageElements) {
        
        chatHistory += messageElement.textContent + "\n";
    }

    return chatHistory.trim();
}

window.onload = preloadModel; 
