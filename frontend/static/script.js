const API_URL = "http://127.0.0.1:8080/api/run"; // Flask endpoint

const form = document.getElementById("chat-form");
const promptInput = document.getElementById("prompt");
const messages = document.getElementById("messages");
const sendBtn = document.getElementById("send");

function addMessage(text, who) {
  const div = document.createElement("div");
  div.className = `msg ${who}`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function sendPrompt(prompt) {
  addMessage(prompt, "user");
  sendBtn.disabled = true;
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });
    const data = await res.json();
    addMessage(data.error ? `Error: ${data.error}` : (data.response || "(no response)"), "bot");
  } catch (e) {
    addMessage(`Network error: ${e.message}`, "bot");
  } finally {
    sendBtn.disabled = false;
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const prompt = promptInput.value.trim();
  if (!prompt) return;
  promptInput.value = "";
  sendPrompt(prompt);
});

