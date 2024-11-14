function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    if (userInput) {
        appendMessage('user', userInput);

        fetch('/api/send-message', {
            method: 'POST',
            body: JSON.stringify({ message: userInput }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => appendMessage('bot', data.response))
        .catch(error => console.error('Error:', error));
        
        document.getElementById('user-input').value = '';
    }
}

function appendMessage(sender, text) {
    let messageContainer = document.createElement('div');
    messageContainer.classList.add('message', `${sender}-message`);
    messageContainer.textContent = `${sender.charAt(0).toUpperCase() + sender.slice(1)}: ${text}`;
    document.getElementById('messages').appendChild(messageContainer);
}

// Function to get the query parameter value
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Retrieve the selected item
const selectedItem = getQueryParam('selectedItem');

// Display or use the selected item
if (selectedItem) {
    console.log("Selected Model:", selectedItem);
    // You can use the selected item in your chatBot.html logic
    document.getElementById('selectedModelDisplay').textContent = `Selected Model: ${selectedItem}`;
}