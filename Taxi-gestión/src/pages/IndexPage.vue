<template>
  <q-page padding class="body-dark">
    <p><pre>{{taxiStore.user[0]}}</pre></p>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted } from "vue";

const taxiStore = useTaxiStore();
onMounted: {
  taxiStore.usuario();
}
</script>
