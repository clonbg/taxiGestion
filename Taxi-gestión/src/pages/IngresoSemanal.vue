<template>
  <q-page padding>
    <h3>Página de ingresos semanales</h3>
  </q-page>
</template>

<!-- <template>
  <q-page padding>
    <h3>Página de ingresos diarios</h3>
    <p><pre>{{ diariosTaxi }}</pre></p>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, computed, ref } from "vue";

const taxiStore = useTaxiStore();

const diariosTaxi = ref([]);

onMounted(async () => {
  await taxiStore.get_ingresos_diarios();
  const tmp = taxiStore.diarios.forEach((element) => {
console.log(localStorage.getItem('email_taxi_user'))
    if (element.taxista?.email == localStorage.getItem('email_taxi_user')) {
      diariosTaxi.value.push(element);
    }
  });
});
</script> -->
