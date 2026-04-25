// static/js/script.js
const form = document.querySelector('form[target="resultsFrame"]');
const themeSelect = document.getElementById("theme");
const citySelect = document.getElementById("city");

// Submit into the iframe when either dropdown changes
function submitToIframeIfReady() {
  // Only submit when BOTH are selected
  if (themeSelect.value && citySelect.value) {
    form.requestSubmit(); // submits form to the iframe target
  }
}

themeSelect.addEventListener("change", submitToIframeIfReady);
citySelect.addEventListener("change", submitToIframeIfReady);