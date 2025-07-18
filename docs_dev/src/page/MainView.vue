<template>
  <div class="home-view">
    <Transition name="header-fade">
      <Header v-show="showHeader && swiperTitle" :panel-title="swiperTitle" />
    </Transition>
    <div class="home-content">
      <swiper :pagination="{
        clickable: true,
      }" :modules="[Pagination, Mousewheel]" :direction="'vertical'" class="mySwiper" mousewheel @swiper="onSwiper"
        @slide-change="changeSlideEmit">
        <swiper-slide>
          <Home />
        </swiper-slide>
        <swiper-slide class="swiper-content">
          <div class="schedule">
            <Gantt />
          </div>
        </swiper-slide>
        <swiper-slide class="swiper-content">
          <Deployment />
        </swiper-slide>
        <swiper-slide class="swiper-content">
          <Frontend />
        </swiper-slide>
        <swiper-slide class="swiper-content">
          <Backend />
        </swiper-slide>
        <swiper-slide class="swiper-content">
          <FinetuneModel />
        </swiper-slide>
      </swiper>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Swiper, SwiperSlide } from 'swiper/vue';
// Import Swiper styles
import 'swiper/css';
import 'swiper/css/pagination';
// import required modules
import { Pagination, Mousewheel } from 'swiper/modules';

import Gantt from '@/components/Gantt.vue'
import Header from '@/components/Header.vue';
import Home from '@/components/Home.vue';
import { ref } from 'vue';
import Frontend from '@/components/demo/Frontend.vue';
import Backend from '@/components/demo/Backend.vue';
import FinetuneModel from '@/components/demo/FinetuneModel.vue';
import Deployment from '@/components/demo/Deployment.vue';

const swiperTitle = ref('')
const showHeader = ref(true)
const swiperObj = ref()

const onSwiper = (swiper: any) => {
  swiperObj.value = swiper
}
const changeSlideEmit = () => {
  const currentSlide = swiperObj.value.activeIndex
  if (currentSlide === 0) {
    showHeader.value = false
  } else {
    showHeader.value = true
  }
  const panelTitle = ['', '-Schedule', '-Deployment Progress', '-Frontend Progress','-Backend Progress', '-Fine-tuning Progress']
  swiperTitle.value = panelTitle[currentSlide]
}

</script>

<style scoped lang="scss">
.home-view {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;

  .home-content {
    width: 100%;
    height: 0px;
    flex: 1;

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

    .swiper-content {
      /* background: #0c0c0c; */
    }

    .swiper-slide img {
      display: block;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .schedule {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;

      .text {
        width: 100%;
        height: 100px;
        display: flex;
      }
    }
  }

  .header-fade-enter-active,
  .header-fade-leave-active {
    transition: height 0.3s ease;
    overflow: hidden;
  }

  .header-fade-enter-from,
  .header-fade-leave-to {
    height: 0;
  }

  .header-fade-enter-to,
  .header-fade-leave-from {
    height: 50px;
    /* 根据你 Header 实际高度调整 */
  }

}
</style>