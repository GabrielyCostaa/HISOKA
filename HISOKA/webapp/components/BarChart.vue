<template>
  <div ref="charBarEl">s</div>
</template>

<script setup lang="ts">
import uPlot from "uplot";
import "uplot/dist/uPlot.min.css";
import { onMounted } from "vue";

const charBarEl = ref<HTMLElement | null>(null);
let u: uPlot | null = null;

function makeChart(data, series) {
  u?.destroy
  const opts = {
    width: 800,
    height: 400,
    scales: {
      y: {
        range: [0, null],
        ori: 1
      },
    },
    axes: [
      {
        	// rotate: -45,
      },
      {
        //	show: false,
        side: 3
      },
    ],
    legend: {
      live: false,
      markers: {
        width: 0,
      },
    },
    padding: [null, 0, null, 0],
    series,
  };

  u = new uPlot(opts, data, document.body);
}

onMounted(() => {
  let data = [
    ["Group A", "Group B", "Group C", "Group D"],
    [1, 2, 3, 10],
    [3, 2, 1, 10],
    [5, 9, 3, 10],
  ];

  let series = [
    {},
    {
      label: "Metric 1",
      fill: "#33BB55",
      width: 0,
    },
    {
      label: "Metric 2",
      fill: "#B56FAB",
      width: 0,
    },
    {
      label: "Metric 3",
      fill: "#BB1133",
      width: 0,
    },
  ];

  makeChart(u, data, series);
  document.body.appendChild(document.createElement("div"));
});

</script>

<style scoped>
.uplot {
  display: inline-block;
  vertical-align: top;
}

.uplot .legend .series:first-child,
.uplot .legend .series th::after,
.uplot .legend .series td {
  display: none;
}

.hidden {
  color: silver;
}

.bar-mark {
  position: absolute;
  background: rgba(255, 255, 255, 0.3);
}
</style>
