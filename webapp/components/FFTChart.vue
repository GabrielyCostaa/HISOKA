<template>
  <div class="bg-neutral-50 border-neutral-100 border-4 rounded-2xl p-2">
    <canvas ref="fftCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch, ref, computed } from "vue";
import { useSensorStore } from "~/stores/sensor";
import Chart from "chart.js/auto";

interface FFTProps {
  sensorIds: string[];
  windowSec: number;
  sampleRate: number;
  colors?: string[];
}

const props = defineProps<FFTProps>();
const fftCanvas = ref<HTMLCanvasElement | null>(null);
let chart: Chart | null = null;

const sensorStore = useSensorStore();

// Função simples de FFT
function calculateFFT(data: number[], sampleRate: number) {
  const N = data.length;
  const fft = new Array(N).fill(0).map(() => ({ re: 0, im: 0 }));

  for (let k = 0; k < N / 2; k++) {
    let re = 0;
    let im = 0;
    for (let n = 0; n < N; n++) {
      const angle = (2 * Math.PI * k * n) / N;
      re += data[n] * Math.cos(angle);
      im -= data[n] * Math.sin(angle);
    }
    fft[k] = { re, im };
  }

  const amplitudes = fft.slice(0, N / 2).map((c) => Math.sqrt(c.re ** 2 + c.im ** 2) / N);
  const frequencies = Array.from({ length: N / 2 }, (_, i) => i * (sampleRate / N));

  return { frequencies, amplitudes };
}

// Computa FFT de todos os sensores
const fftData = computed(() => {
  const datasets: { label: string; data: number[]; borderColor: string }[] = [];
  let freqLabels: number[] = [];

  props.sensorIds.forEach((id, idx) => {
    const [timestamps, values] = sensorStore.getLastDataSlice(id, props.windowSec);
    if (values.length === 0) return;

    const { frequencies, amplitudes } = calculateFFT(values, props.sampleRate);
    if (freqLabels.length === 0) freqLabels = frequencies;

    datasets.push({
      label: id,
      data: amplitudes,
      borderColor: props.colors?.[idx] || "blue",
    });
  });

  return { labels: freqLabels, datasets };
});

function plotFFT() {
  if (!fftCanvas.value) return;
  if (chart) chart.destroy();

  chart = new Chart(fftCanvas.value, {
    type: "line",
    data: {
      labels: fftData.value.labels,
      datasets: fftData.value.datasets,
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
        tooltip: {
          callbacks: {
            label: function (context) {
              return `Sensor: ${context.dataset.label}, Amp: ${context.raw.toFixed(3)}`;
            },
          },
        },
      },
      scales: {
        x: { title: { display: true, text: "Frequência (Hz)" } },
        y: { title: { display: true, text: "Amplitude" } },
      },
    },
  });
}

watch(fftData, plotFFT, { deep: true });
onMounted(plotFFT);
</script>

<style scoped>
canvas {
  width: 100%;
  height: 300px;
}
</style>
