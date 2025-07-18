// src/composables/useMergeComplete.ts
import { onMounted, onBeforeUnmount } from 'vue';
import { wsService, MergeCompleteEvent } from './wsService';

export function useWSService(cb: (e: MergeCompleteEvent) => void) {
  onMounted(() => {
    wsService.subscribeMergeComplete(cb);
  });
  onBeforeUnmount(() => {
    wsService.unsubscribeMergeComplete(cb);
  });
}
