
document.addEventListener("DOMContentLoaded", function () {
  fetch("/delete-jsons", {
      method: "POST",
  })
  .then(response => response.json())
  .then(data => console.log(data.message))
  .catch(error => console.error("Error deleting jsons folder:", error));
});

const sessionId = `session-${Date.now()}`;
let events = [];

rrweb.record({
  emit(event) {
    events.push(event);
  },
});

function save() {
    fetch(`${BASE_URL}/api/save-json`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId, events }),
    })
    .then((response) => response.json())
    .then((data) => console.log("Saved:", data))
    .catch((error) => console.error("Error saving:", error));

    events = []; // Clear events after sending
}



setInterval(save, 10 * 1000);

window.saveRecordedSession = function(){
    fetch(`${BASE_URL}/api/generate-video`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId })
    })
    .then((response) => response.json())
    .then((data) => console.log("Saved:", data))
    .catch((error) => console.error("Error saving:", error));

}