<template>
  <div class="w-full h-full p-2">
    <canvas ref="canvas" class="w-full h-full"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watchEffect } from 'vue'
import { Chart, BarElement, CategoryScale, LinearScale, BarController, Tooltip, Legend } from 'chart.js'
import { useSensorStore } from '~/stores/sensor'
import { storeToRefs } from 'pinia'

// Registrar componentes necessários do Chart.js
Chart.register(BarElement, CategoryScale, LinearScale, BarController, Tooltip, Legend)

const canvas = ref<HTMLCanvasElement | null>(null)
const sensorStore = useSensorStore()
const { sensorData } = storeToRefs(sensorStore)

let chart: Chart | null = null

// Função de cálculo do RMS
function getRMS(values: number[]): number {
  if (!values.length) return 0
  const sumSquares = values.reduce((acc, v) => acc + v * v, 0)
  return Math.sqrt(sumSquares / values.length)
}

onMounted(async () => {
  await nextTick()
  if (!canvas.value) return

  // Cria gráfico vazio
  chart = new Chart(canvas.value, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Potência RMS',
          data: [],
          backgroundColor: [
            '#60a5fa', // Azul
            '#f472b6', // Rosa
            '#facc15', // Amarelo
            '#34d399', // Verde
            '#a78bfa'  // Roxo
          ],
          borderRadius: 8,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          enabled: true,
        },
      },
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            color: '#fff',
          },
        },
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)',
          },
          ticks: {
            color: '#fff',
          },
        },
      },
    },
  })

  // Atualiza o gráfico automaticamente conforme chegam dados
  watchEffect(() => {
    if (!chart) return
    const ids = Object.keys(sensorData.value)

    chart.data.labels = ids
    chart.data.datasets[0].data = ids.map(id => {
      const [, valuesBuffer] = sensorData.value[id] || []
      const values = valuesBuffer ? valuesBuffer.getBuffer() : []
      return getRMS(values)
    })

    chart.update('none')
  })
})
</script>

<style scoped>
canvas {
  background-color: transparent;
}
</style>
