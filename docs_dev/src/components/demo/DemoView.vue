<template>
  <div class="frontend">
    <div class="timeline" ref="timeline">
      <Timeline :events="props.events" />
    </div>
    <div class="demo-panel">
      <swiper :navigation="true" :modules="[Navigation]" :direction="'horizontal'">
        <swiper-slide v-for="detail in details" :key="detail.description">
          <Card class="timeline-card">
            <template #title>
              <img class="timeline-card-bg" :src="detail.path"></img>
            </template>
            <template #content>
              <div class="description">{{ detail.description }}</div>
            </template>
          </Card>
        </swiper-slide>
      </swiper>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, useTemplateRef } from 'vue';
import Timeline from './Timeline.vue';
import { Card } from 'primevue';
import { Swiper, SwiperSlide } from 'swiper/vue';
// Import Swiper styles
import 'swiper/css';
import 'swiper/css/navigation';
// import required modules
import { Navigation } from 'swiper/modules';

const timelineRef = useTemplateRef('timeline');

const props = defineProps({
  events: Array,
  details: Array<any>,
});

onMounted(() => {
  timelineRef.value!.addEventListener('wheel', function (e) {
    const delta = e.deltaY;
    const up = delta < 0;
    const scrollTop = this.scrollTop;
    const scrollHeight = this.scrollHeight;
    const offsetHeight = this.offsetHeight;

    const isAtTop = scrollTop === 0;
    const isAtBottom = scrollTop + offsetHeight >= scrollHeight;

    if ((up && !isAtTop) || (!up && !isAtBottom)) {
      // 如果还没滚到底部或顶部，就阻止冒泡，防止 swiper 接手
      e.stopPropagation();
    }
  }, { passive: false });
})
</script>

<style scoped lang="scss">
@use "sass:math";
$scrollbar-width: 6px;

.frontend {
  width: 100%;
  height: 100%;
  display: flex;

  .timeline {
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 20px 0px 20px 0;

    /* 整个滚动条 */
    &::-webkit-scrollbar {
      width: $scrollbar-width;
      /* 垂直滚动条宽度 */
      height: $scrollbar-width;
      /* 水平滚动条高度 */
    }

    /* 滚动条轨道（背景） */
    &::-webkit-scrollbar-track {
      background: #f0f0f0;
      border-radius: math.div($scrollbar-width, 2);
    }

    /* 滚动条滑块（thumb） */
    &::-webkit-scrollbar-thumb {
      background: #888;
      border-radius: math.div($scrollbar-width, 2);
    }

    /* 滑块悬停时 */
    &::-webkit-scrollbar-thumb:hover {
      background: #555;
    }
  }

  .demo-panel {
    flex: 1;
    width: 0px;
    height: 100%;
    padding: 0px 40px 0 40px;

    .timeline-card {
      width: 100%;
      /* height: 80%; */
      .timeline-card-bg{
        width: 100%;
        height: fit-content; 
      }
      .description{
        font-family: NerkoOne;
        font-size: 40px;
      }
    }

    .swiper {
      width: 100%;
      height: 100%;
    }

    .swiper-slide {
      text-align: center;
      font-size: 18px;

      /* Center slide text vertically */
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }
}
</style>