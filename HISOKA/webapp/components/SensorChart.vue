<template>
  <div class="p-4">
    <h2 class="text-lg font-bold mb-2">Sensor: {{ props.sensorId }}</h2>
    <div class="flex space-x-4 mb-6">
      <div>
        <UButton
          @click="clearSensorData"
          color="neutral"
          variant="subtle"
          :label="$t('clear')"
        />
      </div>
      <div>
        <label class="block text-sm">Janela (s)</label>
        <USlider v-model="window_sec" :min="1" :max="60" class="w-48" />
        <div>{{ window_sec }} s</div>
      </div>
    </div>
    <div
      ref="chartEl"
      class="chart-container border rounded p-2 w-full h-80"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import uPlot from "uplot";
import "uplot/dist/uPlot.min.css";
import { useSensorStore } from "~/stores/sensor";

const window_sec = ref(10);

// Props
const props = defineProps<{
  sensorId?: string;
  data?: [number[], number[]]; // Optional direct input
}>();

const chartEl = ref<HTMLElement | null>(null);
let u: uPlot | null = null;
let animationFrameId: number | null = null;

const sensorStore = useSensorStore();

function getSensorData(): [number[], number[]] {
  if (props.data) return props.data;
  if (props.sensorId && sensorStore.sensorData[props.sensorId]) {
    // return sensorStore.sensorData[props.sensorId]
    return sensorStore.getLastDataSlice(props.sensorId, window_sec.value);
  }
  return [[], []];
}

function clearSensorData() {
  sensorStore.clearSensorDataById(props.sensorId);
}

function initChart() {
  const [xs, ys] = getSensorData();
  const width = chartEl.value?.clientWidth || 600;
  const height = chartEl.value?.clientHeight || 400;

  const opts: uPlot.Options = {
    width,
    height,
    scales: {
      x: { time: false },
      y: {
        auto: true,
      },
    },
    series: [
      {}, // x axis
      {
        label: "Sensor",
        stroke: "blue",
      },
    ],
    axes: [{ grid: { show: false } }, { grid: { show: true } }],
  };

  if (u) u.destroy();
  u = new uPlot(opts, [xs, ys], chartEl.value!);
}

function startLiveUpdate() {
  const loop = () => {
    const [xs, ys] = getSensorData();
    if (xs.length && ys.length) {
      u?.setData([xs, ys]);
    }
    animationFrameId = requestAnimationFrame(loop);
  };
  loop();
}

onMounted(() => {
  initChart();
  startLiveUpdate();

  window.addEventListener("resize", initChart);
  watch(
    () => props.sensorId,
    () => {
      initChart();
    },
  );
});

onBeforeUnmount(() => {
  if (u) u.destroy();
  if (animationFrameId) cancelAnimationFrame(animationFrameId);
  window.removeEventListener("resize", initChart);
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 20vh;
  overflow: hidden;
}
</style>
