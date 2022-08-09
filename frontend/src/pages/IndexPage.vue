<template>
  <q-page class="flex">
    <div class="absolute-center q-ma-xl">
      <p>ACCESO: {{ taxiStore.token_acceso }}</p>
      <p>REFRESCO: {{ taxiStore.token_refresco }}</p>
      <p><q-btn @click="listaTaxistas">Taxistas</q-btn></p>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { useTaxiStore } from "../stores/taxi-store";
import { api } from "../boot/axios";

export default defineComponent({
  name: "IndexPage",
  setup() {
    const taxiStore = useTaxiStore();
    return {
      taxiStore,
    };
  },
  methods: {
    async listaTaxistas() {
      this.taxiStore.verificaToken(this.taxiStore.token_acceso)
      const config = {
        headers: { Authorization: `Bearer ${this.taxiStore.token_acceso}` },
      };
      await api
        .get("/taxistas/registro/", config)
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err.request);
        });
    },
  },
  mounted() {},
});
</script>
