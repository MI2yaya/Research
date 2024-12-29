// Function to load an HTML file and insert it into an element
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
  