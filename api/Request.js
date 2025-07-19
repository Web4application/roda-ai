// Placeholder for future AI integration
// You can connect this to a FastAPI backend with fetch()

// Example:
// fetch("https://your-backend.com/ask", {
//   method: "POST",
//   headers: { "Content-Type": "application/json" },
//   body: JSON.stringify({ prompt: userInput })
// }).then(res => res.json())
//   .then(data => showResponse(data.reply));
async function askAI(prompt) {
  const response = await fetch("https://your-backend-url/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt })
  });
  const data = await response.json();
  return data.reply;
}

// Modify send button logic
chatButton?.addEventListener('click', async () => {
  const msg = chatInput.value.trim();
  if (msg !== '') {
    const messageNode = document.createElement('p');
    messageNode.innerHTML = `<strong>You:</strong> ${msg}`;
    chatBody.appendChild(messageNode);
    chatInput.value = '';
    chatBody.scrollTop = chatBody.scrollHeight;

    const reply = await askAI(msg);
    const replyNode = document.createElement('p');
    replyNode.innerHTML = `<strong>RODA:</strong> ${reply}`;
    chatBody.appendChild(replyNode);
    chatBody.scrollTop = chatBody.scrollHeight;
  }
});

const response = await fetch("https://your-dart-backend.onrender.com/ask", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: msg })
});
