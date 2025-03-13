let loadedModel = null;
let debounceTimeout = null;
let recognition;
let defaultMessage;
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

const selectedItem = getQueryParam('selectedItem');
const selectedModel = getQueryParam('selectedModel');
const tuned = getQueryParam('tuned');

const customDescription = localStorage.getItem("customDescription") || "N/A";
const customMentalIllness = localStorage.getItem("customMentalIllness") || "N/A";

if (selectedItem == "Custom" && customDescription == "N/A"){
    console.log("Error in storage of desc")
}

document.getElementById("user").addEventListener("submit", function(event) {
    event.preventDefault();
    sendMessage();
});

// Function to preload model
function preloadModel() {
    if (selectedItem && selectedModel && tuned && customDescription && customMentalIllness) {
        fetch(`${BASE_URL}/api/preload-model`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                character: selectedItem,
                model: selectedModel,
                tuned: tuned,
                description:customDescription,
                mentalIllness:customMentalIllness
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                loadedModel = data.model; 
                defaultMessage = data.default;
                console.log(data.message);  
                console.log(data.default);
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
            
            const inputField = document.getElementById("user-input");
            const sendButton = document.getElementById("send-button");
            

            inputField.disabled = true;
            sendButton.disabled = true;

            appendMessage('Therapist In Training', userInput);
            const chatHistory = generateChatHistory(); // dont include . . .
            appendMessage('Virtual Patient',". . .",true);

            document.getElementById('user-input').value = '';

            console.log(chatHistory);

            fetch(`${BASE_URL}/api/send-message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: chatHistory }),  
            })
            .then(response => response.json())
            .then(data => {
                if (data.response) {
                    console.log("Bot response:", data.response);
                    appendMessage('Virtual Patient', data.response);

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

// Function to record user voice
function recordMessage(){
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
        if (!loadedModel) {
            console.error("Model not loaded. Please preload the model first."); // If model not loaded
            return;
        }
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
        if (!SpeechRecognition) {
            alert("Your browser does not support speech recognition.");
            return;
        }

        let inputField = document.getElementById('user-input');
        let recordButton = document.getElementById("record-button");

        if(recordButton.classList.contains("listening")){
            if(recognition) recognition.stop();
            recordButton.textContent = "Record";
            recordButton.classList.remove("listening");
            console.log("user stopped");
        }else{
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = "en-US";

            recognition.onresult = function (event) {
                let transcript = "";
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript + " ";
                }
                inputField.value = transcript.trim(); 
                console.log("succeeded!", transcript);
            };

            recognition.onerror = recognition.onend = function (event) {
                recordButton.textContent = "Record";
                recordButton.classList.remove("listening");
                console.error("Speech Recognition Error:", event.error);
            };
            recordButton.textContent = "Listening";
            recordButton.classList.add("listening");
            recognition.start();
            console.log("started");
        };
    }, 300);
}


//function to generate chat history as csv
window.saveChat = function(){
    let chatHistory = generateChatHistory();
    let lines = chatHistory.split("\n");
    let csvContent = "data:text/csv;charset=utf-8,Message\n";

    csvContent+= `"Background:${defaultMessage.replace(/"/g, '""').replace(/\n/g, ' ')}"\n`;

    lines.forEach(line => {
        csvContent += `"${line.replace(/"/g, '""')}"\n`;
    });

    let encodedUri = encodeURI(csvContent);
    let link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "chat_history.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Function to append a message to the UI
function appendMessage(sender, text, filler=false) {
    const messageContainer = document.createElement('div');
    const chatContainer = document.getElementById('chatbox');
    const senderDictionary={
        "Therapist In Training":"Therapist",
        "Virtual Patient":"Patient"
    }
    if(filler){
        messageContainer.classList.add('message', `${senderDictionary[sender]}-message`,"filler")
        messageContainer.id="filler"
    }else{
        messageContainer.classList.add('message', `${senderDictionary[sender]}-message`);
    }
    messageContainer.innerHTML = `<strong>${sender}:</strong> ${text}`;


    document.getElementById('messages').appendChild(messageContainer);

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Function to generate chat history from UI
function generateChatHistory() {
    const messagesContainer = document.getElementById('messages');
    const messageElements = messagesContainer.getElementsByClassName('message');
    let chatHistory = "";

    for (let messageElement of messageElements) {
        
        let messageText = messageElement.textContent;
        // Replace "Therapist In Training:" with "Therapist:"
        messageText = messageText.replace(/^Therapist In Training:/, "Therapist:");
        
        chatHistory += messageText + "\n";
    }

    return chatHistory.trim();
}

window.onload = preloadModel; 
