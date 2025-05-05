import {load} from '@tauri-apps/plugin-store'

export const userStaticStore = await load('access_token_store.json', {autoSave: false})