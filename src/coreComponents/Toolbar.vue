<template>
  <div class="toolbar-view">
    <Button severity="contrast" class="toolbar-button" v-for="button in buttons" :key="button.title" variant="text"
      @click="redirect(button.path)">
      <FontAwesomeIcon :icon="button.icon"></FontAwesomeIcon>
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
    default: () => [],
  },
})

const redirect = (path: string) => {
  router.push({ path:`/home/${path}` });
}




</script>

<style scoped lang="scss">
.p-button.toolbar-button {
  width: 100%;
  padding-left: 20px;
  padding-right: 20px;
  display: flex;
  justify-content: start;
  /* color: #fff; */
}
</style>