<template>
  <q-page class="flex flex-center">
    <q-date
      v-model="date"
      :events="events"
      class="float-left"
      style="margin-right: 15%"
    />

    <q-form
      v-if="diario.length != 0"
      class="form float-right"
      @submit.prevent="subir()"
      autocorrect="off"
      autocapitalize="off"
      autocomplete="off"
      spellcheck="false"
    >
      <q-img
        :src="`${taxiStore.urlServer}${diario[0]?.imagen}`"
        class="imagen q-my-xl"
        :ratio="16 / 9"
        ><template v-slot:error>
          <div class="absolute-full flex flex-center bg-negative text-white">
            No se puede cargar la imagen
          </div>
        </template>
      </q-img>

      <q-file v-model="file" label="Cambie su foto" filled>
        <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>
      </q-file>

      <div class="row">
        <div class="col-12">
          <q-input
            class="q-my-md"
            standout
            v-model="diario[0].total_efectivo"
            label="Efectivo"
            dense
            :rules="[(val) => (val && val >= 0) || 'Valor no válido']"
          />
        </div>
      </div>

      <q-btn
        class="form-submit"
        type="submit"
        :disable="false"
        :color="true ? 'red' : 'green'"
        >Guardar</q-btn
      >
      <q-btn
        class="form-submit q-ml-md q-my-md"
        @click="
          getUser();
          file = null;
        "
        color="primary"
        >Cancelar</q-btn
      >
    </q-form>
    <div v-else class="float-right">Nada que ver</div>

    {{ diario[0] }}
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref, watchEffect } from "vue";

const taxiStore = useTaxiStore();

const diariosTaxi = ref([]);

const diario = ref(null);

const date = ref(null);

const file = ref(null);
watchEffect(() => {
  diario.value = diariosTaxi.value.filter(
    (dia) => dia.dia.replaceAll("-", "/") == date.value
  );
});

const getHoy = () => {
  let today = new Date();
  let year = today.getFullYear();
  let month = today.getMonth() + 1;
  if (month < 10) {
    month = "0" + month;
  }
  let day = today.getDate();
  date.value = year + "/" + month + "/" + day;
};

const events = ref([]);

const getEvents = () => {
  diariosTaxi.value.forEach((element) => {
    events.value.push(element.dia.replaceAll("-", "/"));
  });
};

onMounted(async () => {
  await taxiStore.get_ingresos_diarios();
  taxiStore.diarios.forEach((element) => {
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      diariosTaxi.value.push(element);
    }
  });
  getHoy();
  diariosTaxi.value.sort(function (a, b) {
    return new Date(b.dia) - new Date(a.dia);
  });
  diario.value = diariosTaxi.value[0];
  getEvents();
});
</script>

<style scoped>
.imagen {
  width: 15rem;
  height: 15rem;
  border: 10px solid #666;
}
</style>
