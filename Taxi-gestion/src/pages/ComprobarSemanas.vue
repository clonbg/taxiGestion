<template>
  <q-page>
    <div class="flex flex-center q-ma-sm q-mt-xl">
      <div class="row float-left" style="margin-right: 15%; width: 15rem">
        <div class="q-gutter-md row">
          <q-select
            filled
            :model-value="taxi"
            use-input
            hide-selected
            fill-input
            input-debounce="0"
            :options="options"
            @filter="filterFn"
            @input-value="setModel"
            hint="Text autocomplete"
            style="width: 250px; padding-bottom: 32px"
            label="Taxista"
          >
            <template v-slot:no-option>
              <q-item>
                <q-item-section class="text-grey"> No results </q-item-section>
              </q-item>
            </template>
          </q-select>
        </div>
        <q-date
          v-model="date"
          :events="events"
          today-btn
          :options="optionsFn"
          :locale="myLocale"
        />
      </div>
      <div v-if="semana[0]">
        <div class="q-pa-md">
          <q-table
            title="Semana"
            dense
            :rows="rows"
            :columns="columns"
            row-key="dias"
            :rows-per-page-options="[0]"
          />
        </div>
        <q-badge
          rounded
          :color="semana[0].suma ? 'green' : 'red'"
          :label="
            semana[0].suma
              ? 'La suma es correcta'
              : dias[0]
              ? 'La suma es incorrecta'
              : 'No hay entradas diarias para esa semana'
          "
          class="q-ml-xl"
        />
      </div>
      <div v-else>No hay ninguna semana aquí, cambie de día o de taxista</div>
    </div>
  </q-page>
</template>
<script setup>
import { ref, onMounted, watchEffect, computed } from "vue";
import { useTaxiStore } from "../stores/taxi-store";
import moment from "moment";
import Chart from "../components/charts/MyChart.vue";

const taxiStore = useTaxiStore();
const date = ref(new Date().toJSON().slice(0, 10).replace(/-/g, "/"));
const taxi = ref(null);
const stringOptions = [];
const options = ref(stringOptions);
const diariosTaxi = ref([]);
const semanalesTaxi = ref([]);
const events = ref([]);
const semana = ref(null);
const dias = ref(null);

const columns = [
  {
    name: "dias",
    required: true,
    label: "Días",
    align: "left",
    field: (row) => row.dias,
    format: (val) => `${val}`,
    sortable: true,
  },
  {
    name: "efectivo",
    align: "left",
    label: "Efectivo",
    field: "efectivo",
    sortable: true,
  },
  { name: "tpv", label: "TPV", field: "tpv", align: "left", sortable: true },
  { name: "apps", label: "Apps", align: "left", field: "apps" },
  { name: "varios", label: "Varios", align: "left", field: "varios" },
];

const rows = computed(() => {
  var tabla = [];
  if (semana.value[0]) {
    tabla = [
      {
        dias:
          semana.value[0].dia_inicio.split("-").reverse().join("/") +
          " a " +
          semana.value[0].dia_fin.split("-").reverse().join("/"),
        efectivo: semana.value[0].total_efectivo_semana,
        tpv: semana.value[0].total_tpv_semana,
        apps: semana.value[0].total_apps_semana,
        varios: semana.value[0].varios_semana,
      },
    ];
  }
  if (dias.value[0]) {
    dias.value.forEach((element) => {
      console.log(element);
      var varios = 0;
      for (var i = 0; i < element.vario.length; i++) {
        if (i % 2 == 0) {
          varios += parseInt(element.vario[i]);
        }
      }
      var item = {
        dias: element.dia.split("-").reverse().join("/"),
        efectivo: element.total_efectivo,
        tpv: element.total_tpv,
        apps: element.total_apps,
        varios: varios,
      };
      tabla.push(item);
    });
  }

  return tabla;
});

const myLocale = {
  days: "Domingo_Lunes_Martes_Miércoles_Jueves_Viernes_Sábado".split("_"),
  daysShort: "Dom_Lun_Mar_Mié_Jue_Vie_Sáb".split("_"),
  months:
    "Enero_Febrero_Marzo_Abril_Mayo_Junio_Julio_Agosto_Septiembre_Octubre_Noviembre_Diciembre".split(
      "_"
    ),
  monthsShort: "Ene_Feb_Mar_Abr_May_Jun_Jul_Ago_Sep_Oct_Nov_Dic".split("_"),
  firstDayOfWeek: 1, // 0-6, 0 - Sunday, 1 Monday, ...
  format24h: true,
  pluralDay: "dias",
};

const optionsFn = (fecha) => {
  return (
    fecha >= "2022/01/01" &&
    fecha <= new Date().toJSON().slice(0, 10).replace(/-/g, "/")
  );
};

const filterFn = (val, update, abort) => {
  update(() => {
    const needle = val.toLocaleLowerCase();
    options.value = stringOptions.filter(
      (v) => v.toLocaleLowerCase().indexOf(needle) > -1
    );
  });
};

const setModel = (val) => {
  taxi.value = val;
};

watchEffect(async () => {
  if (stringOptions.lastIndexOf(taxi.value) != -1) {
    await taxiStore.get_ingresos_diarios();
    diariosTaxi.value = [];
    taxiStore.diarios.forEach((element) => {
      if (element.taxista?.email == taxi.value) {
        diariosTaxi.value.push(element);
      }
    });
    await taxiStore.get_ingresos_semanales();
    semanalesTaxi.value = [];
    taxiStore.semanales.forEach((element) => {
      if (element.taxista?.email == taxi.value) {
        semanalesTaxi.value.push(element);
      }
    });
    events.value = [];
    semanalesTaxi.value.forEach((element) => {
      let fecha1 = moment(element.dia_inicio);
      let fecha2 = moment(element.dia_fin);
      for (; fecha1 <= fecha2; ) {
        events.value.push(fecha1.format("YYYY/MM/DD"));
        fecha1.add(1, "day");
      }
    });
  } else {
    diariosTaxi.value = [];
    semanalesTaxi.value = [];
    events.value = [];
  }
});

watchEffect(() => {
  if (date.value && stringOptions.lastIndexOf(taxi.value) != -1) {
    semana.value = semanalesTaxi.value.filter(
      (t) =>
        moment(t.dia_inicio) <= moment(new Date(date.value)) &&
        moment(t.dia_fin) >= moment(new Date(date.value))
    );
    // aqui los diarios que corresponden a esa semana
    dias.value = diariosTaxi.value
      .filter((t) => {
        return (
          moment(t.dia) <= moment(semana.value[0]?.dia_fin) &&
          moment(t.dia) >= moment(semana.value[0]?.dia_inicio)
        );
      })
      .reverse();
    for (var i = 0; i < dias.value.length; i++) {
      if (dias.value[i].vario.length != 0) {
        let sum = 0;
        for (var j = 0; j < dias.value[i].vario.length; j++) {
          if (j % 2 == 0) {
            sum += parseInt(dias.value[i].vario[j]);
          }
        }
        dias.value[i].total_varios = sum;
      }
    }
    if (dias.value[0]) {
      let sumSemana =
        parseInt(semana.value[0].total_efectivo_semana) +
        parseInt(semana.value[0].total_tpv_semana) +
        parseInt(semana.value[0].total_apps_semana) +
        parseInt(semana.value[0].varios_semana);
      let sumaDias = 0;
      dias.value.forEach((element) => {
        sumaDias +=
          parseInt(element.total_apps) +
          parseInt(element.total_efectivo) +
          parseInt(element.total_tpv);
        if (element.total_varios) {
          sumaDias += element.total_varios;
        }
      });
      if (sumSemana == sumaDias) {
        semana.value[0].suma = true;
      } else semana.value[0].suma = false;
    }
  } else {
    semana.value = "";
    dias.value = "";
  }
});

const listaTaxistas = () => {
  taxiStore.listaUsuarios
    .filter((t) => !t.is_superuser)
    .forEach((element) => {
      let item = element.email;
      stringOptions.push(item);
    });
};
onMounted(() => {
  listaTaxistas();
});
</script>
