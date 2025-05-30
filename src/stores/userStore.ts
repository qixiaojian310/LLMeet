// stores/counter.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      isLoggedIn: false,
      username: '',
    }
  },
  // 也可以这样定义
  // state: () => ({ count: 0 })
  actions: {
    login(username: string) {
      this.isLoggedIn = true;
      this.username = username;
    },
    logout() {
      this.isLoggedIn = false;
      this.username = '';
    }
  },
})