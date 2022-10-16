<template>
  <q-page>
    <div class="q-ma-xl">
      <div class="row">
        <q-select
          class="q-mr-xs"
          filled
          :model-value="taxista1"
          use-input
          hide-selected
          fill-input
          input-debounce="0"
          :options="options1"
          @filter="filterFn1"
          @input-value="setModel1"
          style="width: 250px; padding-bottom: 32px"
          label="Taxista 1"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey"> No results </q-item-section>
            </q-item>
          </template>
        </q-select>
        <q-select
          filled
          :model-value="taxista2"
          use-input
          hide-selected
          fill-input
          input-debounce="0"
          :options="options2"
          @filter="filterFn2"
          @input-value="setModel2"
          style="width: 250px; padding-bottom: 32px"
          label="Taxista 2"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey"> No results </q-item-section>
            </q-item>
          </template>
        </q-select>
      </div>
    </div>
    <div>
      <chart
        :series="series"
        :options="chartOptions"
        :key="componentkey"
      ></chart>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, watchEffect } from "vue";
import { useTaxiStore } from "../stores/taxi-store";
import moment from "moment";
import Chart from "../components/charts/MyChart.vue";

const taxiStore = useTaxiStore();

const taxista1 = ref(null);
let stringOptions1 = [];
const options1 = ref(stringOptions1);
const taxista2 = ref(null);
let stringOptions2 = [];
const options2 = ref(stringOptions2);
const componentkey = ref(0);
var series = [
  {
    name: "",
    data: [31, 40, 28, 51, 42, 109, 100],
  },
  {
    name: "",
    data: [11, 32, 0, 32, 34, 52, 41],
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

const listaTaxistas = () => {
  stringOptions1 = [];
  stringOptions2 = [];
  taxiStore.listaUsuarios
    .filter((t) => !t.is_superuser)
    .forEach((element) => {
      let item = element.email;
      if (taxista2.value != item) {
        stringOptions1.push(item);
      }
      if (taxista1.value != item) {
        stringOptions2.push(item);
      }
    });
};

watchEffect(() => {
  if (typeof taxista1.value === "string") {
    series[0].name = taxista1.value;
    // Traer las entradas diarias que coinciden con este taxista, sumarlas cada día y devolverlo en array
  }
  if (typeof taxista2.value === "string") {
    series[1].name = taxista2.value;
    // Traer las entradas diarias que coinciden con este taxista, sumarlas cada día y devolverlo en array
  }

  if (stringOptions2 != [] || stringOptions1 != []) {
    listaTaxistas();
  }
  componentkey.value += 1; //Update
});

const filterFn1 = (val, update, abort) => {
  update(() => {
    const needle = val.toLocaleLowerCase();
    options1.value = stringOptions1.filter(
      (v) => v.toLocaleLowerCase().indexOf(needle) > -1
    );
  });
};

const filterFn2 = (val, update, abort) => {
  update(() => {
    const needle = val.toLocaleLowerCase();
    options2.value = stringOptions2.filter(
      (v) => v.toLocaleLowerCase().indexOf(needle) > -1
    );
  });
};

const setModel1 = (val) => {
  taxista1.value = val;
};

const setModel2 = (val) => {
  taxista2.value = val;
};

onMounted(() => {
  listaTaxistas();
});
</script>
