import { load } from '@tauri-apps/plugin-store';

export let userStaticStore: Awaited<ReturnType<typeof load>>;

(async function () {
  userStaticStore = await load('user_static_store.json', { autoSave: false });
})();
