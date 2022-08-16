<template>
  <q-page padding class="body-dark">
    <p><pre>{{taxiStore.user}}</pre></p>
    <img v-if="taxiStore.user ? true : false" :src="`${taxiStore.urlServer}${taxiStore.user[0].foto}`" class="imgRedonda"/>
    <img v-else src="imgs/fraguel.jpg" class="imgRedonda"/>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted } from "vue";

const taxiStore = useTaxiStore();

const getUser = async () => {
  await taxiStore.usuario();
};
onMounted: {
  getUser();
}
</script>

<style scoped>
.imgRedonda {
  width: 200px;
  height: 200px;
  border-radius: 1120px;
  border: 10px solid #666;
}
.imgR {
  border-radius: 50%;
}
</style>
