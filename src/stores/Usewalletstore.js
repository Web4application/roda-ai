import { defineStore } from 'pinia'

export const useWalletStore = defineStore('wallet', {
  state: () => ({
    address: null,
    balance: null,
    provider: null,
  }),
  actions: {
    async connectWallet() {
      if (window.ethereum) {
        const provider = new ethers.BrowserProvider(window.ethereum)
        const accounts = await provider.send('eth_requestAccounts', [])
        this.address = accounts[0]
        this.provider = provider
        this.balance = await provider.getBalance(this.address)
      }
    },
  },
})
