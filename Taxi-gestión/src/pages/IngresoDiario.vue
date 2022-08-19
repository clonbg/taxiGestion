<template>
  <q-page padding>
    <div class="row">
      <div class="col-6">
        <div class="flex flex-center q-ma-xl">
          <q-date v-model="date" :events="events" />
        </div>
      </div>
    </div>
    <div class="col-6">{{ diariosTaxi }}</div>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref } from "vue";

const taxiStore = useTaxiStore();

const diariosTaxi = ref([]);

const date = ref(null)

const getHoy = () => {
  let today = new Date()
  let year = today.getFullYear()
  let month = today.getMonth() + 1
  if (month < 10) {
    month = '0' + month
  }
  let day = today.getDate()
  date.value = year + '/' + month + '/' + day
}

const events = ref([])

const getEvents = () => {
  diariosTaxi.value.forEach(element => {
    events.value.push(element.dia.replaceAll('-', '/'))
  });
}

onMounted(async () => {
  await taxiStore.get_ingresos_diarios();
  const tmp = taxiStore.diarios.forEach((element) => {
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      diariosTaxi.value.push(element);
    }
  });
  getHoy();
  getEvents()
});

</script>