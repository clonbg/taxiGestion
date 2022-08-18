<template>
  <q-page padding>
    <div class="row">
      <div class="col-6">
        <div class="flex flex-center q-ma-xl">
          <q-date v-model="date" :events="events" />
        </div>
      </div>
      <div class="col-6">{{ diariosTaxi }}</div>
    </div>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, computed, ref } from "vue";

const taxiStore = useTaxiStore();

const diariosTaxi = ref([]);

const date = ref('2019/02/01')
const events = ['2019/02/01', '2019/02/05', '2019/02/06', '2019/02/09', '2019/02/23']

onMounted(async () => {
  await taxiStore.get_ingresos_diarios();
  const tmp = taxiStore.diarios.forEach((element) => {
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      diariosTaxi.value.push(element);
    }
  });
});
</script>

<style scoped>
.caja {
  width: 100px;
  height: 100px;
  background-color: green;
}
</style>