<template>
  <q-page padding>
    <div class="row">
      <div class="col-6">
        <div class="flex flex-center q-ma-xl">
          <q-date v-model="date" :events="events" />
        </div>
      </div>
      <div class="col-6">{{ diario }}</div>
    </div>
    <div>{{ diariosTaxi }}</div>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref, watchEffect } from "vue";

const taxiStore = useTaxiStore();

const diariosTaxi = ref([]);

const diario = ref(null)

const date = ref(null)

watchEffect(() => { console.log(date.value) }) //asignando

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
  taxiStore.diarios.forEach((element) => {
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      diariosTaxi.value.push(element);
    }
  });
  getHoy();
  diariosTaxi.value.sort(function (a, b) {
    return new Date(b.dia) - new Date(a.dia);
  });
  console.log(diariosTaxi.value[0].dia)
  diario.value = diariosTaxi.value[0]
  //diario.value = diariosTaxi.value.filter((dia) => dia.dia.replaceAll('-', '/') == date.value)
  getEvents()
});

</script>

<style scoped>
.imagen {
  width: 15rem;
  height: 15rem;
  border: 10px solid #666;
}
</style>