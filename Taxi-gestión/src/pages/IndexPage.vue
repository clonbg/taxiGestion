<template>
  <q-page padding>
    <q-btn @click="taxiStore.refresToken()" class="q-ma-md">Refresh</q-btn>
    <q-btn @click="listaUsuarios()" class="q-ma-md">Usuarios</q-btn>
    <q-btn to="/diario" class="q-ma-md" v-if="taxiStore.access_token">Diario</q-btn>
    <q-btn to="/semanal" class="q-ma-md" v-if="taxiStore.access_token">Semanal</q-btn>

    <p>ACCESS: {{ taxiStore.access_token }}</p>
    <p><pre>{{usuarios}}</pre></p>

    <p></p>
  </q-page>
</template>

<script setup>
import { api } from "../boot/axios";
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref } from "vue";

const taxiStore = useTaxiStore();
const usuarios = ref(null);
const listaUsuarios = async () => {
  await taxiStore.refresToken();
  if (taxiStore.access_token) {
    let axiosConfig = {
      headers: {
        Authorization: `Bearer ${taxiStore.access_token}`,
      },
    };
    api
      .get("/taxistas/registro/", axiosConfig)
      .then((res) => {
        console.log(res.data);
        usuarios.value = res.data;
      })
      .catch((err) => {
        console.log(err.request);
      });
  }
};
onMounted: {
  listaUsuarios();
}
</script>
