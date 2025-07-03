<template>
  <div class="toolbar-view">
    <Button
      v-for="button in props.buttons"
      :key="button.title"
      severity="contrast"
      class="toolbar-button"
      variant="text"
      @click="redirect(button.path)"
    >
      <FontAwesomeIcon :icon="button.icon" />
      <p>{{ button.title }}</p>
    </Button>
  </div>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { Button } from 'primevue';
import { ToolbarItem } from '@/types/mainLayout/toolbar';
import { router } from '@/router';

const props = defineProps({
  buttons: {
    type: Array<ToolbarItem>,
    default: () => []
  }
});

const redirect = (path: string) => {
  router.push({ path: `/home/${path}` });
};
</script>

<style scoped lang="scss">
.p-button.toolbar-button {
  width: 100%;
  padding: 1rem 1rem;
  display: flex;
  justify-content: start;
  p {
    margin: 0;
  }
}
</style>
