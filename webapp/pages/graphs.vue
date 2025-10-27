<template>
  <!-- <Serial /> -->
  <div class="h-screen flex flex-col">
    <div class="flex h-2/50">
      <Serial />
      <Tools/>
    </div>
    <div
      class="h-full w-screen grid grid-flow-col grid-row-5 grid-cols-10 border-blue-600"
    >
      <div ref="headerRef" class="border-emerald-600 col-start-1 col-end-9">
        <!-- Gráficos RMS individuais -->
        <div v-for="(sensorId, sensor_index) in sensorIds" :key="sensorId">
          <LineChart 
            class="bg-neutral-50 border-neutral-100 border-4 rounded-2xl"
            :sensorId="sensorId"
            :frequency="frequency"
            :amplitude="amplitude"
            :windowSec="windowSec"
            :sampleRate="sampleRate"
            :color="getThemeColor(colors[sensor_index])"
            :heigth="headerVH[0] / colors.length"
            :width="headerVH[1]"
          />
        </div>

        <!-- Gráfico FFT único com todos os sensores -->
        <div class="mt-4">
          <FFTChart
            :sensorIds="sensorIds"
            :windowSec="windowSec"
            :sampleRate="sampleRate"
            :colors="colors.map(c => getThemeColor(c))"
          />
        </div>
      </div>

      <div class="border-fuchsia-500 col-start-9 col-end-11" ref="wRef">
        <div
          class="h-1/2 bg-neutral-50 border-neutral-100 border-4 rounded-2xl"
        >
           <BarChartFake />
        </div>
        <div
          class="bg-neutral-50 border-neutral-100 border-4 rounded-2xl h-1/2"
        >
          <p>1</p>
          <p>1</p>
          <p>1</p>
          <p>1</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { useSensorStore } from "~/stores/sensor";
import LineChart from "~/components/SensorChart.vue";
import FFTChart from "~/components/FFTChart.vue";
import BarChartFake from "~/components/BarChartFake.vue";

const colors = [
  "--color-first",
  "--color-second",
  "--color-third",
  "--color-fourth",
  "--color-fifth",
];

const frequency = ref(50);
const amplitude = ref(4);
const windowSec = ref(2);
const sampleRate = ref(1000);

const headerRef = ref<HTMLElement | null>(null);
const headerVH = ref([10, 10]);

const wRef = ref<HTMLElement | null>(null);
const wVH = ref([10, 10]);

function updateHeights() {
  if (headerRef.value) {
    headerVH.value = getVH(headerRef.value);
  }
  if (wRef.value) {
    wVH.value = getVH(wRef.value);
  }
}
onMounted(() => {
  updateHeights();
});

const sensorStore = useSensorStore();
const sensorIds = computed(() => Object.keys(sensorStore.sensorData));

function getVH(el: HTMLElement) {
  return [el.clientHeight, el.clientWidth];
}

function getThemeColor(name: string): string {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(name)
    .trim();
}
</script>

<style scoped>
canvas {
  width: 100%;
  height: 300px;
}
</style>
