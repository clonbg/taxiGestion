<template>
  <q-page class="flex flex-center">
    <q-date
      v-model="date"
      :events="events"
      class="float-left"
      style="margin-right: 15%"
    />

    <q-form
      class="form float-right"
      @submit.prevent="subir()"
      autocorrect="off"
      autocapitalize="off"
      autocomplete="off"
      spellcheck="false"
      style="width: 30rem"
    >
      <q-img
        :src="`${taxiStore.urlServer}${imagen}`"
        class="imagen q-my-xl"
        :ratio="16 / 9"
      >
        <template v-slot:error>
          <div class="absolute-full flex flex-center bg-negative text-white">
            No se puede cargar la imagen
          </div>
        </template>
      </q-img>

      <q-file v-model="file" label="Imagen" filled>
        <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>
      </q-file>

      <div class="row">
        <div class="col-12">
          <q-input
            class="q-mt-md"
            standout
            v-model="total_efectivo"
            label="Efectivo"
            dense
            :rules="[
              (val) => (val && val >= 0 && !isNaN(val)) || 'Valor no válido',
            ]"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input
            standout
            v-model="total_tpv"
            label="TPV"
            dense
            :rules="[
              (val) => (val && val >= 0 && !isNaN(val)) || 'Valor no válido',
            ]"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input
            standout
            v-model="total_apps"
            label="Apps"
            dense
            :rules="[
              (val) => (val && val >= 0 && !isNaN(val)) || 'Valor no válido',
            ]"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input standout v-model="varios" label="Varios" dense />
        </div>
      </div>

      <q-btn
        class="form-submit"
        type="submit"
        :disable="saveState"
        :color="saveState ? 'red' : 'green'"
        >Guardar</q-btn
      >
      <q-btn
        class="form-submit q-ml-md q-my-md"
        @click="
          getDiarios();
          file = null;
          imagen = '';
          total_efectivo = '';
          total_tpv = '';
          total_apps = '';
          varios = '';
        "
        color="primary"
        >Cancelar</q-btn
      >
    </q-form>

    <p>
      <br />
    </p>
    <br />

    <br />
    diario:{{ diario[0] }} diarioTaxi:{{ diariosTaxi }} <br /><br />
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref, watchEffect, computed } from "vue";

const taxiStore = useTaxiStore();

const diariosTaxi = ref([]);

const diario = ref(null);

let imagen = ref("");
let total_efectivo = ref("");
let total_tpv = ref("");
let total_apps = ref("");
let varios = ref("");

const date = ref(null);

const file = ref(null);
watchEffect(() => {
  diario.value = diariosTaxi.value.filter(
    (dia) => dia.dia.replaceAll("-", "/") == date.value
  );
  if (diario.value[0]) {
    console.log(diario.value[0].imagen);
    imagen.value = diario.value[0].imagen;
    total_efectivo.value = diario.value[0].total_efectivo;
    total_tpv.value = diario.value[0].total_tpv;
    total_apps.value = diario.value[0].total_apps;
    varios.value = diario.value[0].vario;
  } else {
    imagen.value = "";
    total_efectivo.value = "";
    total_tpv.value = "";
    total_apps.value = "";
    varios.value = "";
  }
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

const getDiarios = async () => {
  await taxiStore.get_ingresos_diarios();
  if (diario.value[0]) {
    diario.value = taxiStore.diarios.filter(
      (dia) => dia.id == diario.value[0].id
    );
  }
};

const saveState = computed(() => {
  if (
    total_efectivo.value ||
    total_efectivo.value < 0 ||
    isNaN(total_efectivo.value) ||
    !total_tpv.value ||
    total_tpv.value < 0 ||
    isNaN(total_tpv.value) ||
    !total_apps.value ||
    total_apps.value < 0 ||
    isNaN(total_apps.value)
  ) {
    return true;
  }
  return false;
});

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
  getEvents();
  diario.value = diariosTaxi.value.filter(
    (dia) => dia.dia.replaceAll("-", "/") == date.value
  );
  console.log(diario.value);
  imagen.value = diario.value[0].imagen;
  total_efectivo.value = diario.value[0].total_efectivo;
  total_tpv.value = diario.value[0].total_tpv;
  total_apps.value = diario.value[0].total_apps;
  varios.value = diario.value[0].vario;
});
</script>

<style scoped>
.imagen {
  width: 15rem;
  height: 15rem;
  border: 10px solid #666;
}
</style>
