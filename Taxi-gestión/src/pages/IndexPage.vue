<template>
  <q-page>
    <div class="flex flex-center">
      <q-form class="form q-my-xl" @submit.prevent="subir()" style="min-width: 600px" autocorrect="off" autocapitalize="off" autocomplete="off" spellcheck="false">
        <q-img :src="`${taxiStore.urlServer}${taxiStore.user.foto}`" class="imagen q-ma-xl" :ratio="16 / 9">
          <template v-slot:error>
            <div class="absolute-full flex flex-center bg-negative text-white">
              No se puede cargar la imagen
            </div>
          </template>
        </q-img>
        <div class="row">
          <div class="col-12">
            <q-file v-model="file" label="Cambie su foto" filled class="q-my-xl">
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
            </q-file>
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input standout v-model="taxiStore.user.nombre" label="Nombre" dense :rules="[
                (val) =>
                  (val && val.length >= 3 && val.length <= 20) ||
                  'Entre 3 y 20 carácteres',
              ]" />
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input standout v-model="taxiStore.user.apellidos" label="Apellidos" dense :rules="[
                (val) =>
                  (val && val.length >= 3 && val.length <= 50) ||
                  'Entre 3 y 50 carácteres',
              ]" />
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input standout v-model="taxiStore.user.dni" label="DNI" dense :rules="[
                (val) =>
                  (val && !nif(val) && nifBd(val)) ||
                  'No es válido o ya existe',
              ]" />
          </div>
        </div>
        <div class="row">
          <div class="col-4">
            <q-input v-model="taxiStore.user.sueldo" standout dense label="Sueldo" suffix="%" disable readonly />
          </div>
          <div class="col-1"></div>
          <div class="col-7">
            <q-input standout v-model="licencia" label="Número de licencia" dense disable readonly />
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input class="q-mt-md" standout v-model="taxiStore.user.email" label="Email" type="email" dense :rules="[
                (val) =>
                  (val &&
                    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) &&
                    emailBd(val)) ||
                  'Email no válido o ya existente',
              ]" />
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input standout v-model="taxiStore.user.phone_number" label="Número de teléfono" dense :rules="[
                (val) =>
                  (val &&
                    !isNaN(val) &&
                    val.length >= 7 &&
                    val.length <= 11 &&
                    tlfBd(val)) ||
                  'Número de teléfono no válido o existente',
              ]" />
          </div>
        </div>
        <q-btn class="form-submit" type="submit" :disable="saveState" :color="saveState ? 'red' : 'green'" :loading="loading[0]">Guardar</q-btn>
        <q-btn class="form-submit q-ml-md" @click="
            getUser();
            file = null;
          " color="primary">Cancelar</q-btn>
      </q-form>
    </div>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref, computed } from "vue";
import { api } from "../boot/axios";
import { Notify } from "quasar";

const loading = ref([false, false, false, false, false, false]);

const progress = ref(false);

const simulateProgress = (number) => {
  // we set loading state
  loading.value[number] = true;

  // simulate a delay
  setTimeout(() => {
    // we're done, we reset loading state
    loading.value[number] = false;
    file.value = null;
    getUser();
    taxiStore.letrero.nombre = taxiStore.user.nombre;
    taxiStore.letrero.apellidos = taxiStore.user.apellidos;
    Notify.create({
      type: "positive",
      message: "Ha sido guardado correctamente",
    });
  }, 3000);
};

const taxiStore = useTaxiStore();

const file = ref(null);

const getUser = async() => {
  await taxiStore.usuario();
};

const saveState = computed(() => {
  if (
    taxiStore.user.nombre.length < 3 ||
    taxiStore.user.nombre.length > 20 ||
    taxiStore.user.apellidos.length < 3 ||
    taxiStore.user.apellidos.length > 50 ||
    nif(taxiStore.user.dni) ||
    !nifBd(taxiStore.user.dni) ||
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(taxiStore.user.email) ||
    isNaN(taxiStore.user?.phone_number) ||
    taxiStore.user.phone_number?.length < 7 ||
    taxiStore.user.phone_number?.length > 11 ||
    !emailBd(taxiStore.user.email) ||
    !tlfBd(taxiStore.user?.phone_number)
  ) {
    return true;
  }
  return false;
});

const licencia = computed(() => {
  if (taxiStore.user.licencia) {
    return taxiStore.user.licencia.num_licencia;
  } else {
    return "---------";
  }
});

const nif = (dni) => {
  var numero;
  var letr;
  var letra;
  var expresion_regular_dni;

  expresion_regular_dni = /^\d{8}[a-zA-Z]$/;

  if (expresion_regular_dni.test(dni) == true) {
    numero = dni.substr(0, dni.length - 1);
    letr = dni.substr(dni.length - 1, 1);
    numero = numero % 23;
    letra = "TRWAGMYFPDXBNJZSQVHLCKET";
    letra = letra.substring(numero, numero + 1);
    if (letra != letr.toUpperCase()) {
      return true;
    } else {
      return false;
    }
  } else {
    return true;
  }
};

const nifBd = (dni) => {
  var usersBd = taxiStore.listaUsuarios
    .filter((item) => item.id !== taxiStore.user.id)
    .filter((item) => item.dni.toUpperCase() == dni.toUpperCase());
  if (usersBd.length == 0) {
    return true;
  }
  return false;
};

const emailBd = (email) => {
  var usersBd = taxiStore.listaUsuarios
    .filter((item) => item.id !== taxiStore.user.id)
    .filter((item) => item.email.toUpperCase() == email.toUpperCase());
  if (usersBd.length == 0) {
    return true;
  }
  return false;
};

const tlfBd = (tlf) => {
  var usersBd = taxiStore.listaUsuarios
    .filter((item) => item.id !== taxiStore.user.id)
    .filter((item) => item.phone_number == tlf);
  if (usersBd.length == 0) {
    return true;
  }
  return false;
};

const subir = async() => {
  await taxiStore.refresToken();
  if (taxiStore.access_token) {
    let axiosConfig = {
      headers: {
        Authorization: `Bearer ${taxiStore.access_token}`,
      },
    };
    var formData = new FormData();
    formData.append("dni", taxiStore.user.dni.toUpperCase());
    formData.append("nombre", taxiStore.user.nombre);
    formData.append("apellidos", taxiStore.user.apellidos);
    formData.append("sueldo", taxiStore.user.sueldo);
    if (file.value) {
      formData.append("foto", file.value);
    }
    if (taxiStore.user.licencia) {
      formData.append("licencia_id", parseInt(taxiStore.user.licencia.id));
    }
    formData.append("email", taxiStore.user.email);
    formData.append("phone_number", taxiStore.user.phone_number);

    await api
      .put(`/taxistas/${taxiStore.user.id}/`, formData, axiosConfig)
      .then(async(res) => {
        simulateProgress(0);
      })
      .catch((err) => {
        console.log(err.response);
        Notify.create({
          type: "negative",
          message: JSON.stringify(err.response.data.detail),
        });
      });
  }
};
onMounted(() => {
  getUser();
});
</script>

<style scoped>
.imagen {
  width: 15rem;
  height: 15rem;
  border: 10px solid #666;
}
</style>
