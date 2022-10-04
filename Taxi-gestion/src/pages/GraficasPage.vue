<template>
  <q-page class="flex flex-center q-ma-sm">
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
    <div><pre>{{semana[0]}}</pre></div>
  </q-page>
</template>
<script setup>
import { ref, onMounted, watchEffect } from "vue";
import { useTaxiStore } from "../stores/taxi-store";
import moment from "moment";

const taxiStore = useTaxiStore();
const date = ref(new Date().toJSON().slice(0, 10).replace(/-/g, "/"));
const taxi = ref(null);
const stringOptions = [];
const options = ref(stringOptions);
const diariosTaxi = ref([]);
const semanalesTaxi = ref([]);
const events = ref([]);
const semana = ref();

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
      if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
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
  console.log(taxi.value, diariosTaxi.value, semanalesTaxi.value, events.value);
});

watchEffect(() => {
  if (date.value && stringOptions.lastIndexOf(taxi.value) != -1) {
    semana.value = semanalesTaxi.value.filter(
      (t) =>
        moment(t.dia_inicio) <= moment(new Date(date.value)) &&
        moment(t.dia_fin) >= moment(new Date(date.value))
    );
    // aqui los diarios que corresponden a esa semana
  } else {
    semana.value = '';
  }
  console.log("cambia de día", semana.value);
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
