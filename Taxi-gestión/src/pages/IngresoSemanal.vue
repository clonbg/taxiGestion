<template>
  <q-page class="flex flex-center">
    <p><pre>{{ date }}</pre></p>
    <p><pre>{{ semanalesTaxi }}</pre></p>
    <q-date
      v-model="date"
      :events="events"
      class="float-left"
      style="margin-right: 15%"
      today-btn
      :options="optionsFn"
      :locale="myLocale"
    />
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, computed, ref } from "vue";
import moment from 'moment';

const taxiStore = useTaxiStore();
const semanalesTaxi = ref([]);
const date = ref([]);
const hoy =ref(null)
const events = ref([])


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

const getHoy = () => {
  let today = new Date();
  let year = today.getFullYear();
  let month = today.getMonth() + 1;
  if (month < 10) {
    month = "0" + month;
  }
  let day = today.getDate();
  if (day < 10) {
    day = "0" + day;
  }
  date.value = year + "/" + month + "/" + day;
  hoy.value = date.value;
};

const getEvents = () => {
  semanalesTaxi.value.forEach((element) => {
    let fecha1 = moment(element.dia_inicio)
    let fecha2 = moment(element.dia_fin)
    let resta = fecha2.from(fecha1)
    console.log(fecha1.format(), fecha2.format(), resta);
    for (var i = 0; fecha1<=fecha2; i++) {
      events.value.push(fecha1.format("YYYY/MM/DD"))
      fecha1.add(1,'day')
    }
  });
  //events.value.push(element.dia.replaceAll("-", "/"));
};

onMounted(async () => {
  await taxiStore.get_ingresos_semanales();
  taxiStore.semanales.forEach((element) => {
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      semanalesTaxi.value.push(element);
    }
  });
  getHoy()
  semanalesTaxi.value.sort(function (a, b) {
    return new Date(b.dia_fin) - new Date(a.dia_fin);
  });
  getEvents();
  /*diario.value = diariosTaxi.value.filter(
    (dia) => dia.dia.replaceAll("-", "/") == date.value
  );*/
});
</script>
