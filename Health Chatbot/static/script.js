const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function appendMessage(text, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${sender}`;
  const textSpan = document.createElement('span');
  textSpan.className = 'text';
  textSpan.textContent = text;
  messageDiv.appendChild(textSpan);
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
  const userText = userInput.value.trim();
  if (userText) {
    appendMessage(userText, 'user');
    userInput.value = '';

    // Update the fetch URL here
    try {
      const response = await fetch("http://127.0.0.1:5000/chat", { // Use 127.0.0.1 here
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText }),
      });

      const data = await response.json();
      if (response.ok) {
        appendMessage(data.response, 'assistant');
      } else {
        appendMessage("Error: " + (data.error || "Failed to connect to chatbot."), 'assistant');
      }
    } catch (error) {
      appendMessage("Error: Could not connect to the server.", 'assistant');
    }
  }
}

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});
