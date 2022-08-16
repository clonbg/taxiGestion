<template>
  <q-page padding>
    <div class="row q-ma-md q-ml-md">
      <form class="form" @submit.prevent="editarUsuario()">
        <img v-if="(taxiStore.user[0].foto) ? true : false" :src="`${taxiStore.urlServer}${taxiStore.user[0].foto}`"
          class="imgRedonda" />
        <img v-else src="imgs/fraguel.jpg" class="imgRedonda" />
        <q-input label="Label (stacked)" stack-label dense name="asdf" />
        <q-btn class="form-submit" type="submit">Save</q-btn>
      </form>

    </div>

    <div class="q-gutter-md row items-start">

    </div>
    <p>
    <pre>{{ taxiStore.user }}</pre>
    </p>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted } from "vue";
import { api } from '../boot/axios'

const taxiStore = useTaxiStore();

const getUser = async () => {
  await taxiStore.usuario();
};

const editarUsuario = () => {
  const formData = new FormData();
  Object.entries(taxiStore.user[0]).forEach(element => {
    formData.append(element[0], element[1])
  });

  //console.log("Form Data");
  for (let obj of formData) {
    //console.log(obj);
  }

  //console.log(JSON.stringify(formData));
  subir()

}

const subir = async () => {
  await taxiStore.refresToken();
  if (taxiStore.access_token) {
    let axiosConfig = {
      headers: {
        Authorization: `Bearer ${taxiStore.access_token}`
      },
    };
    const data = {
      "dni": "taxijefe@freeallapp.com",
      "nombre": "taxijefe@freeallapp.",
      "apellidos": "taxijefe@freeallapp.com",
      "sueldo": 6,
      "foto": null,
      "licencia_id": null,
      "email": "taxijefe@freeallapp.com",
      "phone_number": null,
    }
    console.log(axiosConfig)
    api
      .put("/taxistas/7/", data, axiosConfig)
      .then(async (res) => {
        await taxiStore.usuario()
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
.imgRedonda {
  width: 15rem;
  height: 15rem;
  border-radius: 30rem;
  border: 10px solid #666;
}

.imgR {
  border-radius: 50%;
}
</style>
