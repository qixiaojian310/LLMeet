import { createApp } from "vue";
import { createPinia } from 'pinia'

import App from "./App.vue";
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import 'primeicons/primeicons.css'
import { router } from "./router";
import ToastService from 'primevue/toastservice';
import ConfirmationService from 'primevue/confirmationservice'
import DialogService from 'primevue/dialogservice'

const app = createApp(App);
const pinia = createPinia();
app.use(PrimeVue, {
  theme: {
    preset: Aura
  },
});
app.use(pinia).use(router).use(ToastService).use(ConfirmationService).use(DialogService);
app.mount("#app");
