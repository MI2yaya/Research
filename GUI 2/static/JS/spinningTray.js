localStorage.removeItem("customDescription");
localStorage.removeItem("customMentalIllness");
localStorage.removeItem("customAge");
console.log("Cleared Storage")

const items = [
    { title: 'Model 1', description: 'Proof of Concept model to show capabilities, accessability, and form a chain of thought.', mentalIllness: 'Major Depressive Disorder', age: '65' },
    { title: 'Model 2', description: 'Proof of Concept model for Anxiety', mentalIllness: 'Generalized Anxiety', age: '50' },
    { title: 'Custom', description: 'Enter Desc.', mentalIllness: 'Enter Mental Illness', age: 'Enter Age Range' }
    //{ title: 'M', description: 'Description of Item 4', mentalIllness: 'TBA', age: 'TBA' },
];

let currentIndex = 0;
let selectedModel = null;

const itemTitle = document.getElementById('itemTitle');
const itemDescription = document.getElementById('itemDescription');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');
const itemForm = document.getElementById('itemForm');
const tunedCheckbox = document.getElementById("tunedCheckbox");
const tunedCheckboxText = document.getElementById("tunedCheckBoxText")

const defaultMentalIllness = document.getElementById('itemMentalIllness')
const defaultAge = document.getElementById('itemAge')
const defaultDescription = document.getElementById('itemDescription')

const customMentalIllness = document.getElementById('custom-mentalIllness')
const customDescription = document.getElementById('custom-description')

const itemDisplay = document.querySelector('.item-display');

// Function to update the item display
function updateItemDisplay() {
    itemTitle.textContent = items[currentIndex].title; //Set the individual aspects
    itemDescription.textContent = items[currentIndex].description;
    defaultMentalIllness.textContent = `Mental Illness: ${items[currentIndex].mentalIllness}`;
    defaultAge.textContent = `Age: ${items[currentIndex].age}`;

    // If "Custom" is selected, show input fields
    if (items[currentIndex].title === "Custom") {
        customDescription.style.display = "block";
        customMentalIllness.style.display = "block";

        defaultAge.style.display = "none";
        defaultDescription.style.display = "none";
        defaultMentalIllness.style.display = "none";
        tunedCheckboxText.style.display = "none";

    } else {
        customDescription.style.display = "none";
        customMentalIllness.style.display = "none";

        defaultAge.style.display = "block";
        defaultDescription.style.display = "block";
        defaultMentalIllness.style.display = "block";
        tunedCheckboxText.style.display = "block";
    }


    // Ensure proper centering
    itemDisplay.style.display = "flex";
    itemDisplay.style.flexDirection = "column";
    itemDisplay.style.justifyContent = "center";
    itemDisplay.style.alignItems = "center";
    itemDisplay.style.textAlign = "center";
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

// Add event listeners to model buttons
document.querySelectorAll('.modelButton').forEach(button => {
    button.addEventListener('click', (event) => {
        // Remove "selected" class from all buttons
        document.querySelectorAll('.modelButton').forEach(btn => btn.classList.remove('selected'));

        // Add "selected" class to the clicked button
        event.target.classList.add('selected');

        // Update the selected model
        selectedModel = event.target.getAttribute('data-model');
    });
});

// Event listener for the submit button
submitBtn.addEventListener('click', () => {

    if (!selectedModel) {
        alert('Please select an ML model before submitting.');
        return;
    }

    // Update the hidden input value
    updateSelectedItem();

    // I mean I can just pass this as storage........................ maybe if I feel like it
    document.getElementById('selectedModel').value = selectedModel;

    // Redirect to chatBot.html with the selected item as a query parameter
    const selectedItem = document.getElementById("selectedItem").value;
    let tuned = tunedCheckbox.checked;
    console.log(tuned)
    if (items[currentIndex].title === 'Custom') {
        localStorage.setItem('customDescription', customDescription.value);
        localStorage.setItem('customMentalIllness', customMentalIllness.value);
        tuned = "N/A";

        if (!customDescription.value && !customMentalIllness.value){
            alert('Please Enter All Fields! Or Select a Different Model.');
            return;
        }
    }

    window.location.href = `/chatBot?selectedItem=${encodeURIComponent(selectedItem)}&selectedModel=${encodeURIComponent(selectedModel)}&tuned=${encodeURIComponent(tuned)}`;
});

// Function to update the hidden input value
function updateSelectedItem() {
    const itemTitle = document.getElementById("itemTitle").textContent;
    document.getElementById("selectedItem").value = itemTitle;
}


updateItemDisplay();