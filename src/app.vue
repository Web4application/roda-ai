<template>
  <div id="roda-app">
    <header>
      <h1>🤖 RODA AI Interface</h1>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/wallet">Wallet</router-link>
        <router-link to="/swap">Swap</router-link>
        <router-link to="/chat">AI Chat</router-link>
      </nav>
    </header>

    <main>
      <router-view />
    </main>

    <footer>
      <p>© {{ currentYear }} RODA AI — Powering the Web4 future.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const currentYear = new Date().getFullYear()
</script>

<style>
#roda-app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #0e0e0e;
  color: #eee;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  padding: 1rem 2rem;
  background: #1a1a1a;
  border-bottom: 2px solid #2a2a2a;
}

header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #00ffd0;
}

nav {
  margin-top: 0.5rem;
}

nav a {
  margin-right: 1rem;
  text-decoration: none;
  color: #ccc;
}

nav a.router-link-exact-active {
  color: #00ffd0;
  font-weight: bold;
}

main {
  flex: 1;
  padding: 2rem;
}

footer {
  padding: 1rem;
  background: #1a1a1a;
  text-align: center;
  font-size: 0.9rem;
  color: #777;
}
</style>
