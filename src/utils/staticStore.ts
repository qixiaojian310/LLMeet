import { load } from '@tauri-apps/plugin-store';

export const userStaticStore = await load('user_static_store.json', { autoSave: false });
