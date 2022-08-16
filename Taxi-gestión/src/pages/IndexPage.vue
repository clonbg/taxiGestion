<template>
  <q-page padding>
    <div class="row q-ma-md q-ml-md">
    <img v-if="taxiStore.user ? true : false" :src="`${taxiStore.urlServer}${taxiStore.user[0].foto}`" class="imgRedonda"/>
    <img v-else src="imgs/fraguel.jpg" class="imgRedonda"/>
    </div>

    <div class="q-gutter-md row items-start">
      <q-uploader
        style="max-width: 300px"
        label="Restricted to images"
        multiple
        accept=".jpg, image/*"
        max-files="1"
        @rejected="onRejected"
        :factory="subirImagen"
      />
    </div>
    <p><pre>{{taxiStore.user}}</pre></p>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted } from "vue";
import { useQuasar } from "quasar";
const $q = useQuasar();

const onRejected = (rejectedEntries) => {
  // Notify plugin needs to be installed
  // https://quasar.dev/quasar-plugins/notify#Installation
  $q.notify({
    type: "negative",
    message: `Sólo se permite una imagen`,
  });
};

const taxiStore = useTaxiStore();

const getUser = async () => {
  await taxiStore.usuario();
};

const subirImagen = (imagen) => {
  console.log(imagen);
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
