<template>
  <q-page class="flex flex-center">
    <q-date
      v-model="date"
      :events="events"
      class="float-left"
      style="margin-right: 10%"
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
            v-model="diario[0].total_efectivo"
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
            v-model="diario[0].total_tpv"
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
            v-model="diario[0].total_apps"
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
          <q-input
            standout
            v-model="diario[0].varios"
            label="Varios"
            dense
            :rules="[
              (val) =>
                (val && (val >= -100000) & (val <= 100000)) ||
                'Valor no válido',
            ]"
          />
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
        "
        color="primary"
        >Cancelar</q-btn
      >
    </q-form>
    <div v-else class="float-right">Nada que ver</div>
    diario:{{ diario[0] }}
    <p><br /></p>
    <br /><br />
    diarioTaxi:{{ diariosTaxi }}
    <p>Falta el subir(), state de varios</p>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref, watchEffect, computed } from "vue";

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

const getDiarios = async () => {
  await taxiStore.get_ingresos_diarios();
  diario.value = taxiStore.diarios.filter(
    (dia) => dia.id == diario.value[0].id
  );
};

const saveState = computed(() => {
  if (
    !diario.value[0].total_efectivo ||
    diario.value[0].total_efectivo < 0 ||
    isNaN(diario.value[0].total_efectivo) ||
    !diario.value[0].total_tpv ||
    diario.value[0].total_tpv < 0 ||
    isNaN(diario.value[0].total_tpv) ||
    !diario.value[0].total_apps ||
    diario.value[0].total_apps < 0 ||
    isNaN(diario.value[0].total_apps)
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
});
</script>

<style scoped>
.imagen {
  width: 15rem;
  height: 15rem;
  border: 10px solid #666;
}
</style>
