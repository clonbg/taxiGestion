<template>
  <q-page padding>
    <h3>Página de ingresos semanales</h3>
        <p><pre>{{ semanalesTaxi }}</pre></p>

  </q-page>
</template>


<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, computed, ref } from "vue";

const taxiStore = useTaxiStore();

const semanalesTaxi = ref([]);

onMounted(async () => {
  await taxiStore.get_ingresos_semanales()
  taxiStore.semanales.forEach((element) => {
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      semanalesTaxi.value.push(element);
    }
  });
});
</script>
