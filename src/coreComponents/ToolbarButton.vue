<template>
  <div class="toolbar-button" @click="handleClick" v-tooltip="isMini ? props.title : undefined">
    <FontAwesomeIcon :icon="props.icon" :style="{ fontSize: isMini ? '1.5rem' : '2rem' }" />
    <span v-if="!props.isMini">{{ props.title }}</span>
  </div>
</template>

<script setup lang="ts">
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
const props = defineProps<{
  title: string;
  icon: IconDefinition;
  handleClick?: () => void;
  isMini?: boolean;
}>();
</script>

<style lang="scss" scoped>
.toolbar-button {
  all: unset;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  background-color: transparent;
  border: none;
  color: var(--secondary-text-color);
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.3s;
  &:hover {
    color: var(--secondary-hover-color);
  }
  span {
    text-align: center;
  }
}
</style>
