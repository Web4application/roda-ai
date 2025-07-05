// Toggle assistant widget
function launchAssistant() {
  document.getElementById('chat-widget').classList.remove('hidden');
}

function closeAssistant() {
  document.getElementById('chat-widget').classList.add('hidden');
} 

// Optional: scroll chat body to bottom on send
const chatInput = document.querySelector('.chat-input input');
const chatButton = document.querySelector('.chat-input button');
const chatBody = document.querySelector('.chat-body');

chatButton?.addEventListener('click', () => {
  const msg = chatInput.value.trim();
  if (msg !== '') {
    const messageNode = document.createElement('p');
    messageNode.innerHTML = `<strong>You:</strong> ${msg}`;
    chatBody.appendChild(messageNode);
    chatInput.value = '';
    chatBody.scrollTop = chatBody.scrollHeight;
  }
});
