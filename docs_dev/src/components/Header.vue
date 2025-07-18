<template>
  <div class="header">
    <div class="title">
      <img class="icon" src="/llmeet-icon.png" alt="">
      <p>LLMeet</p>
      <p>{{ props.panelTitle }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  panelTitle: String
})
</script>

<style scoped>
.header {
  padding: 0px 10px 0px 0px;
  width: 100%;
  .title{
    width: 500px;
    display: flex;
    align-items: center;
    justify-content: start;
    .icon{
      width: 50px;
      height: 50px;
      margin-right: 10px;
    }
    p{
      font-family: NerkoOne;
      font-size: 16px;
      font-weight: 700;
      color: var( --primary-text-color);
      margin: 0px 00px 0px 0px;
      padding: 0px;
    }
  }
}
</style>