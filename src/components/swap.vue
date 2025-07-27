<template>
  <section class="swap">
    <h2>🔄 Token Swap</h2>
    <input v-model="amount" placeholder="Enter FDAK amount" />
    <button @click="swapTokens">Swap FDAK → FX</button>

    <p v-if="result">Transaction Hash: {{ result }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const amount = ref('')
const result = ref('')

function swapTokens() {
  // Placeholder logic for swap
  result.value = '0xSWAP123456789ABCDEF'
}
</script>

<style scoped>
.swap {
  background: #111;
  padding: 2rem;
  border: 1px solid #333;
  border-radius: 8px;
}
input {
  padding: 0.5rem;
  margin-bottom: 1rem;
  width: 60%;
}
button {
  padding: 0.5rem 1rem;
  background: #00ffd0;
  color: black;
  font-weight: bold;
  border: none;
}
</style>
