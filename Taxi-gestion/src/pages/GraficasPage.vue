<template>
  <q-page>
    <div class="q-ma-xl">
      <div class="row">
        <q-select
          class="q-mr-xs"
          filled
          v-model="taxista1"
          :options="options1"
          @filter="filterFn1"
          style="width: 250px; padding-bottom: 32px"
          label="Taxista 1"
          behavior="menu"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey"> No results </q-item-section>
            </q-item>
          </template>
        </q-select>
        <q-select
          class="q-mr-xs"
          filled
          v-model="taxista2"
          :options="options2"
          @filter="filterFn2"
          style="width: 250px; padding-bottom: 32px"
          label="Taxista 2"
          behavior="menu"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey"> No results </q-item-section>
            </q-item>
          </template>
        </q-select>
        <q-input
          class="q-mr-xs"
          standout
          v-model.number="anyo"
          type="number"
          label="Año"
          filled
          :rules="[
            ((val) => val && !isNaN(val) && val >= 2022 && val <= 2200) ||
              'Año no válido',
          ]"
        />
        <q-select
          filled
          v-model="mes"
          :options="optionsMeses"
          style="width: 250px; padding-bottom: 32px"
          label="Mes"
          behavior="menu"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey"> No results </q-item-section>
            </q-item>
          </template>
        </q-select>
      </div>
    </div>
    <div class="q-mr-md">
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
const anyo = ref(new Date().getFullYear());
const optionsMeses =
  "Enero_Febrero_Marzo_Abril_Mayo_Junio_Julio_Agosto_Septiembre_Octubre_Noviembre_Diciembre".split(
    "_"
  );
const mes = ref(optionsMeses[new Date().getMonth()]);
var series = [
  {
    name: "",
    data: [],
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
    categories: [],
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

const getDiarios = async () => {
  await taxiStore.get_ingresos_diarios();
  // for del mes con los días
  // si hay entrada diaria del taxista 1 o 2 se añade a su data
  // si no añadimos un cero
};

watchEffect(() => {
  getDiarios();
  console.log(taxiStore.diarios);
  if (typeof taxista1.value === "string") {
    series[0].name = taxista1.value;
    // Traer las entradas diarias que coinciden con este taxista, sumarlas cada día y devolverlo en array
  }
  if (typeof taxista2.value === "string") {
    series[1].name = taxista2.value;
    // Traer las entradas diarias que coinciden con este taxista, sumarlas cada día y devolverlo en array
  }
  if (
    anyo.value &&
    !isNaN(anyo.value) &&
    anyo.value >= 2022 &&
    anyo.value <= 2200
  ) {
    //días tiene el mes
    let num_dias_mes = new Date(
      anyo.value,
      optionsMeses.indexOf(mes.value) + 1,
      0
    ).getDate();
    chartOptions.xaxis.categories = [];
    for (var i = 1; i <= num_dias_mes; i++) {
      let item = `${anyo.value}-${
        optionsMeses.indexOf(mes.value) >= 9
          ? optionsMeses.indexOf(mes.value) + 1
          : "0" + (optionsMeses.indexOf(mes.value) + 1).toString()
      }-${i > 9 ? i : "0" + i.toString()}`;
      chartOptions.xaxis.categories.push(item);
    }
  } else chartOptions.xaxis.categories = [];
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

onMounted(() => {
  listaTaxistas();
});
</script>
