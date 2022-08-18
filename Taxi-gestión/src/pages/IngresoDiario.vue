<template>
  <q-page padding>
    <div class="row">
      <div class="col-6">Aquí quiero poner el calendario y en el otro las entradas</div>
      <div class="col-6">{{ diariosTaxi }}</div>
    </div>
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
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      diariosTaxi.value.push(element);
    }
  });
});
</script>
