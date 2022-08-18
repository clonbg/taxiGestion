<template>
  <q-page>
    <div class="flex flex-center">
      <form
        class="form q-my-xl"
        @submit.prevent="subir()"
        style="min-width: 600px"
      >
        <q-img
          :src="`${taxiStore.urlServer}${taxiStore.user.foto}`"
          class="imagen q-ma-xl"
          :ratio="16 / 9"
          ><template v-slot:error>
            <div class="absolute-full flex flex-center bg-negative text-white">
              No se puede cargar la imagen
            </div>
          </template>
        </q-img>
        <div class="row">
          <div class="col-12">
            <q-file
              v-model="file"
              label="Cambie su foto"
              filled
              class="q-my-xl"
            >
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
            </q-file>
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input
              standout
              v-model="taxiStore.user.nombre"
              label="Nombre"
              dense
              :rules="[
                (val) =>
                  (val && val.length >= 3 && val.length <= 20) ||
                  'Entre 3 y 20 carácteres',
              ]"
            />
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input
              standout
              v-model="taxiStore.user.apellidos"
              label="Apellidos"
              dense
              :rules="[
                (val) =>
                  (val && val.length >= 3 && val.length <= 50) ||
                  'Entre 3 y 50 carácteres',
              ]"
            />
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input
              standout
              v-model="taxiStore.user.dni"
              label="DNI"
              dense
              :rules="[
                (val) =>
                  (val && !nif(val) && nifBd(val)) ||
                  'No es válido o ya existe',
              ]"
            />
          </div>
        </div>
        <div class="row">
          <div class="col-4">
            <q-input
              v-model="taxiStore.user.sueldo"
              standout
              dense
              label="Sueldo"
              suffix="%"
              disable
              readonly
            />
          </div>
          <div class="col-1"></div>
          <div class="col-7">
            <q-input
              standout
              v-model="licencia"
              label="Número de licencia"
              dense
              disable
              readonly
            />
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input
              class="q-mt-md"
              standout
              v-model="taxiStore.user.email"
              label="Email"
              type="email"
              dense
              :rules="[
                (val) =>
                  (val && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) ||
                  'Email no válido',
              ]"
            />
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <q-input
              standout
              v-model="taxiStore.user.phone_number"
              label="Número de teléfono"
              dense
              :rules="[
                (val) =>
                  (val && !isNaN(val) && val.length >= 7 && val.length <= 11) ||
                  'Número de teléfono no válido',
              ]"
            />
          </div>
        </div>
        <q-btn
          class="form-submit"
          type="submit"
          :disable="saveState"
          :color="saveState ? 'red' : 'green'"
          >Save</q-btn
        >
      </form>
    </div>
    <p>
      seguir con el formulario y las validaciones y notificación error y ok - Si
      es igual que no grabe - Probar con usuario nuevo sin datos - el email y el
      num_telef no exista
    </p>
    <pre>{{ taxiStore.user }}</pre>
    <pre>{{ `${taxiStore.urlServer}${taxiStore.user.foto}` }}</pre>
    <pre>{{ taxiStore.listaUsuarios }}</pre>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref, computed } from "vue";
import { api } from "../boot/axios";

const taxiStore = useTaxiStore();

const file = ref(null);

const getUser = async () => {
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
    isNaN(taxiStore.user.phone_number) ||
    taxiStore.user.phone_number.length < 7 ||
    taxiStore.user.phone_number.length > 11
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

const subir = async () => {
  await taxiStore.refresToken();
  if (taxiStore.access_token) {
    let axiosConfig = {
      headers: {
        Authorization: `Bearer ${taxiStore.access_token}`,
      },
    };
    var formData = new FormData();
    formData.append("dni", taxiStore.user.dni);
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

    console.log(axiosConfig);
    await api
      .put(`/taxistas/${taxiStore.user.id}/`, formData, axiosConfig)
      .then(async (res) => {
        file.value = null;
        getUser();
        console.log(taxiStore.user);
        taxiStore.letrero.nombre = taxiStore.user.nombre;
        taxiStore.letrero.apellidos = taxiStore.user.apellidos;
        console.log(res);
      })
      .catch((err) => {
        console.log(err.response);
      });
  }
};
onMounted: {
  getUser();
}
</script>

<style scoped>
.imagen {
  width: 15rem;
  height: 15rem;
  border: 10px solid #666;
}
</style>
