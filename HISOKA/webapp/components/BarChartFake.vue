<template>
  <div ref="chartContainer" class="w-full h-full p-2 overflow-hidden"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watchEffect, onBeforeUnmount } from 'vue'
import uPlot from 'uplot'
import 'uplot/dist/uPlot.min.css'
import { useSensorStore } from '~/stores/sensor'
import { storeToRefs } from 'pinia'

const chartContainer = ref<HTMLDivElement | null>(null)
const sensorStore = useSensorStore()
const { sensorData } = storeToRefs(sensorStore)

let chart: uPlot | null = null
let resizeObserver: ResizeObserver | null = null

function getRMS(values: number[]): number {
  if (!values.length) return 0
  const sumSquares = values.reduce((acc, v) => acc + v * v, 0)
  return Math.sqrt(sumSquares / values.length)
}

const colors = [
  '#60a5fa', '#f87171', '#34d399', '#facc15',
  '#a78bfa', '#fb923c', '#2dd4bf', '#f472b6',
]

onMounted(async () => {
  await nextTick()
  if (!chartContainer.value) return

  const opts: uPlot.Options = {
    title: 'RMS por Sensor',
    width: chartContainer.value.clientWidth,
    height: chartContainer.value.clientHeight,
    legend: { show: false },

    axes: [
      {
        stroke: '#fff',
        grid: { stroke: 'rgba(255,255,255,0.1)' },
        values: (u, vals) => vals.map(v => `${v} V`) // ticks com "V"
      },
      {
        stroke: '#fff',
        grid: { stroke: 'rgba(255,255,255,0.1)' },
        scale: 'y',
        values: (u, vals) => vals.map(v => v.toFixed(2)),
      },
    ],

    scales: {
      y: { range: [0, 3] },
    },

    series: [
      {}, // eixo X
      {
        label: 'RMS',
        stroke: 'none',
        fill: 'transparent',
        width: 0,
        paths: (u, seriesIdx) => {
          const [xVals, yVals] = [u.data[0], u.data[seriesIdx]]
          const ctx = u.ctx
          const yScale = u.valToPos
          const baseY = yScale(0, 'y', true)

          const maxBarWidth = 20 // barras mais finas
          const gap = 20
          const totalBarsWidth = xVals.length * maxBarWidth + (xVals.length - 1) * gap
          const startX = (u.bbox.width - totalBarsWidth) / 2

          ctx.save()
          ctx.font = '10px sans-serif'
          ctx.textAlign = 'center'

          for (let i = 0; i < xVals.length; i++) {
            const x = startX + i * (maxBarWidth + gap)
            const y = yScale(yVals[i], 'y', true)

            ctx.fillStyle = colors[i % colors.length]
            ctx.fillRect(x, y, maxBarWidth, baseY - y)

            // Label do sensor
            ctx.fillStyle = '#fff'
            ctx.fillText(`S${i + 1}`, x + maxBarWidth / 2, baseY + 12)
          }

          ctx.restore()
          return null
        },
      },
    ],
  }

  const data: uPlot.AlignedData = [[], []]
  chart = new uPlot(opts, data, chartContainer.value)

  watchEffect(() => {
    if (!chart) return

    const ids = Object.keys(sensorData.value)
    if (ids.length === 0) {
      chart.setData([[], []])
      return
    }

    const rmsValues = ids.map(id => {
      const [, valuesBuffer] = sensorData.value[id] || []
      const values = valuesBuffer ? valuesBuffer.getBuffer() : []
      return getRMS(values)
    })

    const xData = ids.map((_, i) => i + 1)
    chart.setData([xData, rmsValues])
  })

  resizeObserver = new ResizeObserver(() => {
    if (chart && chartContainer.value) {
      chart.setSize({
        width: chartContainer.value.clientWidth,
        height: chartContainer.value.clientHeight,
      })
    }
  })
  resizeObserver.observe(chartContainer.value)
})

onBeforeUnmount(() => {
  if (resizeObserver && chartContainer.value)
    resizeObserver.unobserve(chartContainer.value)
  chart?.destroy()
})
</script>

<style scoped>
.uplot {
  background: transparent;
}
</style>
