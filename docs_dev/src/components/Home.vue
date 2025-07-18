<template>
  <div class="home">
    <div class="home-bg">
      <!-- 更大、更丰富的波浪 SVG -->
      <svg class="wave-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 200" preserveAspectRatio="none">
        <defs>
          <linearGradient id="wave-gradient" gradientTransform="rotate(90)">
            <stop offset="0%" stop-color="#005A9E" />
            <stop offset="100%" stop-color="#00B3FF" />
          </linearGradient>
          <!-- 把原来 path 的 d 放在这里 -->
          <path id="wave-path" d="M0,60 C200,10 400,110 600,60 C800,10 1000,110 1200,60 L1200,200 L0,200 Z"/>
        </defs>
        <g class="wave-group">
          <use href="#wave-path" x="0" fill="url(#wave-gradient)" />
          <use href="#wave-path" x="1200" fill="url(#wave-gradient)" />
          <!-- 同理也可以再加一层白色半透明浪花 -->
          <use href="#wave-path" x="0" fill="rgba(255,255,255,0.3)" transform="translate(0,20) scale(1,0.5)" />
          <use href="#wave-path" x="1200" fill="rgba(255,255,255,0.3)" transform="translate(0,20) scale(1,0.5)" />
        </g>
      </svg>

    </div>
    <div class="home-container">
      <div class="title">
        <img class="icon" src="/llmeet-icon.png" alt="" />

        <p>LLMeet</p>
      </div>
      <div class="sub-title">
        <p>
          A powerful tool for your team to organize your meeting and convert
          summarization.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// import AsciiVideo from './AsciiVideo.vue';
</script>

<style scoped lang="scss">
.home {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  color: #f1f1f1;

  .home-bg {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      135deg,
      #00254a 0%,
      #005a9e 50%,
      #00b3ff 100%
    );
    top: -20px; left: -20px;
    width: calc(100% + 40px);
    height: calc(100% + 40px);
    filter: blur(10px);
    opacity: 1;
    z-index: -1;
  }

  .wave-svg {
    position: absolute;
    bottom: -20px;
    left: 0;
    width: 200%;
    height: 200px;
    /* 提升成独立图层，触发 GPU 加速 */
    will-change: transform;
    backface-visibility: hidden;
    animation: wave-slide 8s linear infinite;
  }

  @keyframes wave-slide {
    from { transform: translate3d(0, 0, 0); }
    to   { transform: translate3d(-50%, 0, 0); }
  }


  .home-container {
    width: 80%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;

    .title {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: end;
      height: 150px;
      gap: 10px;
      .icon {
        width: 100px;
        height: 100px;
        border-radius: 10px;
      }

      p {
        font-family: NerkoOne;
        font-size: 50px;
      }
    }

    .sub-title {
      width: 500px;
      text-align: left;

      p {
        font-family: NerkoOne;
        font-size: 20px;
      }
    }
  }
}
</style>
