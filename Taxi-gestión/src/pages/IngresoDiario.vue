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
      <p>
        Imagen obligatoria,maximo dias en el calendario hasta hoy, si ya existe
        put, error en el concepto validacion cuando pones numeros(tampoco
        permite más de 25 caracteres), vario guarda todo en un texto separado
        por comas
      </p>
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
      <span v-for="(item, index) in varios" :key="index">
        <div v-if="index % 2 != 0">
          <div class="row no-wrap">
            <div class="col-4 q-mb-lm q-mr-sm">
              <q-input
                standout
                v-model="varios[index - 1]"
                label="Varios"
                dense
                :rules="[
                  (val) =>
                    (val && val >= 0 && !isNaN(val)) || 'Valor no válido',
                ]"
              />
            </div>
            <div class="col-7">
              <q-input
                standout
                v-model="varios[index]"
                label="Varios"
                dense
                :rules="[
                  (val) => (val && val.length >= 3) || 'Valor no válido',
                ]"
              />
            </div>
            <div class="col-2 nowrap">
              <q-icon
                name="delete"
                color="teal"
                size="3em"
                @click="borrar(index)"
              />
            </div>
          </div>
        </div>
      </span>

      <q-btn
        class="form-submit"
        type="submit"
        :disable="saveState"
        :color="saveState ? 'red' : 'green'"
        >Guardar</q-btn
      >
      <q-btn
        class="form-submit q-ml-md q-my-md"
        @click="getDiarios()"
        color="primary"
        >Cancelar</q-btn
      >
      <q-btn
        :disable="validarVarios()"
        round
        color="purple"
        glossy
        icon="add_task"
        class="float-right q-mt-sm"
        @click="variosMas()"
      />
    </q-form>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref, watchEffect, computed } from "vue";
import { api } from "../boot/axios";

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
  if (diario.value[0]) {
    await taxiStore.get_ingresos_diarios();
    taxiStore.diarios.forEach((element) => {
      diariosTaxi.value = [];
      if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
        diariosTaxi.value.push(element);
      }
      console.log("Por aquí");
    });
    diario.value = diariosTaxi.value.filter(
      (dia) => dia.dia.replaceAll("-", "/") == date.value
    );
  } else {
    imagen.value = "";
    total_efectivo.value = "";
    total_tpv.value = "";
    total_apps.value = "";
    varios.value = "";
  }
  file.value = [];
};

const validarVarios = () => {
  if (varios.value) {
    let array = Object.values(varios.value);
    const found = array.lastIndexOf("") != -1;
    if (varios.value.length > 0 && found) {
      return true;
    } else {
      return false;
    }
  }
};

const saveState = computed(() => {
  if (
    !total_efectivo.value ||
    total_efectivo.value < 0 ||
    isNaN(total_efectivo.value) ||
    !total_tpv.value ||
    total_tpv.value < 0 ||
    isNaN(total_tpv.value) ||
    !total_apps.value ||
    total_apps.value < 0 ||
    isNaN(total_apps.value) ||
    validarVarios()
  ) {
    return true;
  }
  return false;
});

const borrar = (i) => {
  let array = Object.values(varios.value);
  array.splice(i - 1, 1);
  array.splice(i - 1, 1);
  varios.value = array;
};

const variosMas = () => {
  let array = Object.values(varios.value);
  const found = array.lastIndexOf("") == -1;
  if (found) {
    array.push("");
    array.push("");
    varios.value = array;
  }
};

const subir = async () => {
  await taxiStore.refresToken();
  if (taxiStore.access_token) {
    let axiosConfig = {
      headers: {
        Authorization: `Bearer ${taxiStore.access_token}`,
      },
    };
    var formData = new FormData();
    formData.append("dia", date.value.replaceAll("/", "-"));
    formData.append("imagen", file.value);
    formData.append("total_efectivo", total_efectivo.value);
    formData.append("total_apps", total_apps.value);
    formData.append("total_tpv", total_tpv.value);

    if (varios.value.length > 0) {
      for (let i = 0; i < varios.value.length; i++) {
        const element = varios.value[i];
        console.log(`${element}: ${varios.value[element]}`);
        formData.append("vario", element);
      }
    }
    formData.append("taxista_id", taxiStore.user.id);
    await api
      .post(`/ingreso_diario/create/`, formData, axiosConfig)
      .then((res) => {
        file.value = null;
        imagen.value = res.data.imagen;
        date.value = res.data.dia.replaceAll("-", "/");
        diariosTaxi.value.push(res.data);
        getEvents();
      })
      .catch((err) => {
        console.log(err.response);
      });
  }
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
  getEvents();
  diario.value = diariosTaxi.value.filter(
    (dia) => dia.dia.replaceAll("-", "/") == date.value
  );
});
</script>

<style scoped>
.imagen {
  width: 15rem;
  height: 15rem;
  border: 10px solid #666;
}
</style>
