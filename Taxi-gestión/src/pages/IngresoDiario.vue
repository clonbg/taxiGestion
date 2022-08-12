<template>
  <q-page padding>
    <h3>Página de ingresos diarios</h3>
    <h5>{{taxiStore.access_token}}</h5>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from '../stores/taxi-store';

const taxiStore = useTaxiStore()
</script>
