<template>
  <q-page padding>
    <q-btn @click="taxiStore.access()" class="q-ma-md">Ingresar</q-btn>
    <q-btn @click="taxiStore.refresToken()" class="q-ma-md">Refresh</q-btn>
    <q-btn @click="listaUsuarios()" class="q-ma-md">Usuarios</q-btn>
    <q-btn @click="taxiStore.logout()" class="q-ma-md">Logout</q-btn>
    <p>ACCESS: {{ taxiStore.access_token }}</p>

    <p></p>
  </q-page>
</template>

<script setup>
import { api } from "../boot/axios";
import { useTaxiStore } from '../stores/taxi-store';

const taxiStore = useTaxiStore()

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
    })
    .catch((err) => {
      console.log(err.request);
    });
  }

};
</script>
