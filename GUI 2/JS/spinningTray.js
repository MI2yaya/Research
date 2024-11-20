const items = [
    { title: 'Dummy Model', description: 'Proof of Concept model to show capabilities, accessability, and form a chain of thought.', mentalIllness: 'Major Depressive Disorder', age: '65' },
    { title: 'TBA', description: 'Description of Item 2', mentalIllness: 'TBA', age: 'TBA' },
    { title: 'TBA', description: 'Description of Item 3', mentalIllness: 'TBA', age: 'TBA' },
    { title: 'TBA', description: 'Description of Item 4', mentalIllness: 'TBA', age: 'TBA' },
];

let currentIndex = 0;

const itemTitle = document.getElementById('itemTitle');
const itemDescription = document.getElementById('itemDescription');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');
const itemForm = document.getElementById('itemForm');

// Function to update the item display
function updateItemDisplay() {
    itemTitle.textContent = items[currentIndex].title; //Set the individual aspects
    itemDescription.textContent = items[currentIndex].description;
    document.getElementById('itemMentalIllness').textContent = `Mental Illness: ${items[currentIndex].mentalIllness}`;
    document.getElementById('itemAge').textContent = `Age: ${items[currentIndex].age}`;
}

// Event listeners for the buttons
prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + items.length) % items.length;
    updateItemDisplay();
});

nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % items.length;
    updateItemDisplay();
});

// Event listener for the submit button
submitBtn.addEventListener('click', () => {
    // Update the hidden input value
    updateSelectedItem();

    // Redirect to chatBot.html with the selected item as a query parameter
    const selectedItem = document.getElementById("selectedItem").value;
    window.location.href = `chatBot.html?selectedItem=${encodeURIComponent(selectedItem)}`;
});

// Function to update the hidden input value
function updateSelectedItem() {
    const itemTitle = document.getElementById("itemTitle").textContent;
    document.getElementById("selectedItem").value = itemTitle;
}

// Initialize the display
updateItemDisplay();
