import { createMemoryHistory, createRouter } from "vue-router";

import MainLayout from "@/layout/MainLayout.vue";

const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      { path: "/", redirect: "/home" },
      { path: "/home", name: 'home', component: () => import("@/page/HomeView.vue") },
      { path: '/meeting-form', name: 'meetingForm', component: () => import('@/page/MeetingFormView.vue')},
    ],
  },
];

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
});
