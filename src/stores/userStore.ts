// stores/counter.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      isLoggedIn: false,
    }
  },
  // 也可以这样定义
  // state: () => ({ count: 0 })
  actions: {
    login() {
      this.isLoggedIn = true;
    },
    logout() {
      this.isLoggedIn = false;
    }
  },
})