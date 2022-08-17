<template>
  <q-page>
    <div class="flex flex-center">
      <form class="form q-my-xl" @submit.prevent="subir()" style="min-width:600px">
        <q-img :src="`${taxiStore.urlServer}${taxiStore.user.foto}`" class="imagen q-ma-xl" :ratio="16 / 9"><template
            v-slot:error>
            <div class="absolute-full flex flex-center bg-negative text-white">
              No se puede cargar la imagen
            </div>
          </template>
        </q-img>
        <q-file v-model="file" label="Cambie su foto" filled class="q-my-md">
          <template v-slot:prepend>
            <q-icon name="attach_file" />
          </template>
        </q-file>
        <q-input standout v-model="taxiStore.user.nombre" label="Nombre" dense class="q-my-lg" />
        <q-input standout v-model="taxiStore.user.apellidos" label="Apellidos" dense class="q-my-lg" />
        <q-btn class="form-submit" type="submit">Save</q-btn>
      </form>
    </div>
    <p>Falta el nombre y apellidos del navbar, seguir con el formulario, cambiar la id, y las validaciones y
      notificación error y ok</p>
    <pre>{{ taxiStore.user }}</pre>
    <pre>{{ `${taxiStore.urlServer}${taxiStore.user.foto}` }}</pre>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, ref } from "vue";
import { api } from '../boot/axios'

const taxiStore = useTaxiStore();

const file = ref(null)

const getUser = async () => {
  await taxiStore.usuario();
};


const subir = async () => {
  await taxiStore.refresToken();
  if (taxiStore.access_token) {
    let axiosConfig = {
      headers: {
        Authorization: `Bearer ${taxiStore.access_token}`
      },
    };
    var formData = new FormData();
    formData.append('dni', taxiStore.user.dni)
    formData.append("nombre", taxiStore.user.nombre)
    formData.append("apellidos", taxiStore.user.apellidos)
    formData.append("sueldo", taxiStore.user.sueldo)
    if (file.value) {
      formData.append("foto", file.value)
    }
    if (taxiStore.user.licencia) {
      formData.append("licencia_id", parseInt(taxiStore.user.licencia.id))
    }
    formData.append("email", taxiStore.user.email)
    formData.append("phone_number", taxiStore.user.phone_number)

    console.log(axiosConfig)
    await api
      .put(`/taxistas/${taxiStore.user.id}/`, formData, axiosConfig)
      .then(async (res) => {
        file.value = null
        getUser()
        console.log(res)
      })
      .catch((err) => {
        console.log(err.request.response);
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
