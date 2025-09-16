const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const toggleBtn = document.getElementById("toggleTheme");

// Append messages to chatbox
function appendMessage(sender, text) {
  let msgDiv = document.createElement("div");
  msgDiv.classList.add("msg", sender);
  msgDiv.innerHTML = text;
  chatbox.appendChild(msgDiv);
  chatbox.scrollTop = chatbox.scrollHeight;
}

// Send message
async function sendMessage() {
  let input = userInput.value.trim();
  if (!input) return;

  appendMessage("user", input);

  let res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: input })
  });

  let data = await res.json();
  appendMessage("bot", data.reply);

  if (data.tasks && data.tasks.length > 0) {
    appendMessage("bot", "📋 Tasks: " + data.tasks.join(", "));
  }

  userInput.value = "";
}

// Events
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => { if (e.key === "Enter") sendMessage(); });

// Toggle theme
toggleBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  document.body.classList.toggle("light");
  toggleBtn.textContent = document.body.classList.contains("dark") ? "🌙" : "☀️";
});
