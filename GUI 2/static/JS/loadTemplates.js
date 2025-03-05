// Function to load an HTML file and insert it into an element
const BASE_URL = window.location.hostname === '127.0.0.1' ? 'http://127.0.0.1:5000' : 'https://ai-psychotherapy-training-deployment.onrender.com';

function loadHTML(url, elementId) {
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to load ${url}: ${response.statusText}`);
        }
        return response.text();
      })
      .then(data => {
        document.getElementById(elementId).innerHTML = data;
      })
      .catch(error => {
        console.error('Error loading template:', error);
      });
  }
  
  // Load the header into the page
  document.addEventListener('DOMContentLoaded', () => {
    loadHTML('/static/header.html', 'header');
    loadHTML('/static/footer.html', 'footer');
  });
  