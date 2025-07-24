<template>
  <section class="chat">
    <h2>💬 Ask RODA AI</h2>
    <textarea v-model="userInput" placeholder="Type your question..."></textarea>
    <button @click="sendMessage">Send</button>

    <div class="chat-log" v-if="reply">
      <p><strong>You:</strong> {{ userInput }}</p>
      <p><strong>RODA:</strong> {{ reply }}</p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const userInput = ref('')
const reply = ref('')

function sendMessage() {
  // Simulate AI reply
  reply.value = "I'm always listening, RODA is ready. 🤖"
}
</script>

<style scoped>
.chat {
  padding: 2rem;
}
textarea {
  width: 100%;
  height: 80px;
  padding: 0.5rem;
  margin-bottom: 1rem;
}
button {
  padding: 0.5rem 1rem;
  background: #00ffd0;
  color: black;
  font-weight: bold;
  border: none;
}
.chat-log {
  background: #222;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 8px;
}
</style>
