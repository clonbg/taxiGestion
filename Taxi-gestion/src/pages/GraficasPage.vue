<template>
  <q-page>
    <div class="q-ma-xl">
      <chart :series="series" :options="chartOptions"></chart>
    </div>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import moment from "moment";
import Chart from "../components/charts/MyChart.vue";

const series = [
  {
    name: "taxista1",
    data: [31, 40, 28, 51, 42, 109, 100],
  },
  {
    name: "taxista2",
    data: [11, 32, 45, 32, 34, 52, 41],
  },
];

const chartOptions = {
  chart: {
    height: 350,
    type: "area",
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "smooth",
  },
  xaxis: {
    type: "datetime",
    categories: [
      "2018-09-19",
      "2018-09-20",
      "2018-09-21",
      "2018-09-22",
      "2018-09-23",
      "2018-09-24",
      "2018-09-25",
    ],
  },
  tooltip: {
    x: {
      format: "dd/MM/yy",
    },
  },
};
</script>
