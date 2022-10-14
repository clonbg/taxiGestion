<template>
  <q-page>
    <div class="q-ma-xl">
      <div class="q-gutter-md row">
        <q-select
          filled
          :model-value="taxista1"
          use-input
          hide-selected
          fill-input
          input-debounce="0"
          :options="options"
          @filter="filterFn"
          @input-value="setModel"
          hint="Text autocomplete"
          style="width: 250px; padding-bottom: 32px"
          label="Taxista 1"
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
const stringOptions = [];
const options = ref(stringOptions);
const componentkey = ref(0);
var series = [
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

watchEffect(() => {
  if (typeof taxista1.value === "string") {
    series[0].name = taxista1.value;
    // Traer las entradas diarias que coinciden con este taxista, sumarlas cada día y devolverlo en array
    componentkey.value += 1; //Update
  }
});

const filterFn = (val, update, abort) => {
  update(() => {
    const needle = val.toLocaleLowerCase();
    options.value = stringOptions.filter(
      (v) => v.toLocaleLowerCase().indexOf(needle) > -1
    );
  });
};

const listaTaxistas = () => {
  taxiStore.listaUsuarios
    .filter((t) => !t.is_superuser)
    .forEach((element) => {
      let item = element.email;
      stringOptions.push(item);
    });
};

const setModel = (val) => {
  taxista1.value = val;
};

onMounted(() => {
  listaTaxistas();
});
</script>
