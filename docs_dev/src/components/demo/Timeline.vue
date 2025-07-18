<template>
  <Timeline :value="props.events">
    <template #marker="slotProps">
      <span
        class="flex w-8 h-8 items-center justify-center text-white rounded-full z-10 shadow-sm"
        :style="{ backgroundColor: slotProps.item.color }"
      >
        <FontAwesomeIcon :icon="faDotCircle" />
      </span>
    </template>
    <template #content="slotProps">
      <Card class="timeline-card">
        <template #title>
          {{ slotProps.item.status }}
        </template>
        <template #subtitle>
          {{ slotProps.item.date }}
        </template>
        <template #content>
          <img
            v-if="slotProps.item.image"
            :src="`https://primefaces.org/cdn/primevue/images/product/${slotProps.item.image}`"
            :alt="slotProps.item.name"
            width="200"
            class="shadow-sm"
          />
          <p>
            {{ slotProps.item.text }}
          </p>
        </template>
      </Card>
    </template>
  </Timeline>
</template>

<script setup lang="ts">
import { faDotCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { Timeline, Card } from "primevue";
const props = defineProps({
  events: Array,
});
</script>

<style lang="scss" scoped>
.timeline-card {
  margin: 10px 0px;
  width: 400px;
}
</style>
