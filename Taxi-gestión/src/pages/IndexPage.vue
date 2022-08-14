<template>
  <q-page padding>
    <q-btn @click="taxiStore.refresToken()" class="q-ma-md">Refresh</q-btn>
    <q-btn @click="taxiStore.usuario()" class="q-ma-md">Usuarios</q-btn>
    <q-btn to="/diario" class="q-ma-md" v-if="taxiStore.access_token">Diario</q-btn>
    <q-btn to="/semanal" class="q-ma-md" v-if="taxiStore.access_token">Semanal</q-btn>

    <p>ACCESS: {{ taxiStore.access_token }}</p>
    <p><pre>{{taxiStore.user}}</pre></p>

    <p></p>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";

const taxiStore = useTaxiStore();
</script>
