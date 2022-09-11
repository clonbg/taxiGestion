<template>
  <q-page class="flex flex-center">
    <q-date
      v-model="dates"
      class="float-left"
      style="margin-right: 15%"
      :locale="myLocale"
      range multiple
    />
  </q-page>
</template>


<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, computed, ref } from "vue";

const taxiStore = useTaxiStore();

const semanalesTaxi = ref([]);

const dates = ref([{ from: '2022/09/01', to: '2022/09/10' },
        { from: '2022/09/21', to: '2022/09/25' }])

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

onMounted(async () => {
  await taxiStore.get_ingresos_semanales()
  taxiStore.semanales.forEach((element) => {
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      semanalesTaxi.value.push(element);
    }
  });
});
</script>
