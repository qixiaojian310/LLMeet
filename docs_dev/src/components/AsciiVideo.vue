<template>
  <div class="ascii-video">
    <input type="file" accept="video/*" @change="handleFileChange" />
    <video ref="videoRef" :src="bgVideo" autoplay muted loop playsinline style="display: none" />
    <canvas ref="canvasRef" :width="width" :height="height" style="display: none" />
    <pre ref="asciiRef" class="ascii-output"></pre>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import bgVideo from '@/assets/bg.mp4'

const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const asciiRef = ref<HTMLElement | null>(null)

const width = 120
const height = 60
const chars = "@%#*+=-:. " // 从暗到亮的字符

const handleFileChange = (e: Event) => {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (file && videoRef.value) {
    const url = URL.createObjectURL(file)
    videoRef.value.src = url
  }
}

const renderFrame = () => {
  const video = videoRef.value
  const canvas = canvasRef.value
  const pre = asciiRef.value
  if (!video || !canvas || !pre) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.drawImage(video, 0, 0, width, height)
  const imageData = ctx.getImageData(0, 0, width, height).data

  let asciiStr = ''
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const index = (y * width + x) * 4
      const r = imageData[index]
      const g = imageData[index + 1]
      const b = imageData[index + 2]
      const gray = 0.2126 * r + 0.7152 * g + 0.0722 * b
      const char = chars[Math.floor((gray / 255) * (chars.length - 1))]
      asciiStr += char
    }
    asciiStr += '\n'
  }  
  pre.textContent = asciiStr
  requestAnimationFrame(renderFrame)
}

onMounted(() => {
  videoRef.value?.addEventListener('play', () => {
    requestAnimationFrame(renderFrame)
  })
})
</script>

<style scoped>
.ascii-video {
  font-family: monospace;
  background: black;
  color: white;
}

.ascii-output {
  white-space: pre;
  font-size: 6px;
  line-height: 80%;
}
</style>
