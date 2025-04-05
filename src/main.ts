import { createApp } from "vue";
import App from "./App.vue";
import PrimeVue from 'primevue/config';
import Material from '@primeuix/themes/material';
import 'primeicons/primeicons.css'
import { router } from "./router";
import ToastService from 'primevue/toastservice';
import ConfirmationService from 'primevue/confirmationservice'
import DialogService from 'primevue/dialogservice'


const app = createApp(App);
app.use(PrimeVue, {
  theme: {
    preset: Material
  },
});
app.use(router).use(ToastService).use(ConfirmationService).use(DialogService);
app.mount("#app");
