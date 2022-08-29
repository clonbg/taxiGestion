<template>
  <q-page class="flex flex-center">
    <q-date v-model="date" :events="events" class="float-left" style="margin-right: 15%" today-btn :options="optionsFn" />
    <q-form class="form float-right" @submit.prevent="subir()" autocorrect="off" autocapitalize="off" autocomplete="off" spellcheck="false" style="width: 30rem">
      <!-- <p>si ya existe put (Si existe en getEvents...)</p>
      <p>Obligatorio al crear user. Password al inscribirse</p>
      <p>Retardo en el login</p>
      <p>Retardo al guardar</p>
      <p>Dos decimales</p>
      <p>Imagen no se puede actualizar</p> -->
      <q-img :src="`${taxiStore.urlServer}${imagen}`" class="imagen q-my-xl" :ratio="16 / 9">
        <template v-slot:error>
          <div class="absolute-full flex flex-center bg-negative text-white">
            No se puede cargar la imagen
          </div>
        </template>
      </q-img>
      <q-file v-model="file" label="Inserte o cambie la imagen" filled :rules="[
              (val) =>
                (events.indexOf(date)==-1 ? val : true) ||
                'La imagen es obligatoria',
            ]">
        <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>
      </q-file>
      <div class="row">
        <div class="col-12">
          <q-input class="q-mt-md" standout v-model="total_efectivo" label="Efectivo" dense :rules="[
              (val) =>
                (val && val >= 0 && !isNaN(val) && val <= 1000000) ||
                'Valor no válido',
            ]" />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input standout v-model="total_tpv" label="TPV" dense :rules="[
              (val) =>
                (val && val >= 0 && !isNaN(val) && val <= 1000000) ||
                'Valor no válido',
            ]" />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input standout v-model="total_apps" label="Apps" dense :rules="[
              (val) =>
                (val && val >= 0 && !isNaN(val) && val <= 1000000) ||
                'Valor no válido',
            ]" />
        </div>
      </div>
      <span v-for="(item, index) in varios" :key="index">
        <div v-if="index % 2 != 0">
          <div class="row no-wrap">
            <div class="col-4 q-mb-lm q-mr-sm">
              <q-input standout v-model="varios[index - 1]" label="Varios" dense :rules="[
                  (val) =>
                    (val && val >= 0 && !isNaN(val) && val <= 1000000) ||
                    'Valor no válido',
                ]" />
            </div>
            <div class="col-7">
              <q-input standout v-model="varios[index]" label="Varios" dense :rules="[
                  (val) =>
                    (val &&
                      val.toString().length >= 3 &&
                      val.toString().length <= 25) ||
                    'Valor no válido',
                ]" />
            </div>
            <div class="col-2 nowrap">
              <q-icon name="delete" color="teal" size="3em" @click="borrar(index)" />
            </div>
          </div>
        </div>
      </span>
      <q-btn class="form-submit" type="submit" :disable="saveState" :color="saveState ? 'red' : 'green'">Guardar</q-btn>
      <q-btn class="form-submit q-ml-md q-my-md" @click="getDiarios()" color="primary">Cancelar</q-btn>
      <q-btn :disable="validarVarios" round color="purple" glossy icon="add_task" class="float-right q-mt-sm" @click="variosMas()" />
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

const hoy = ref(null);

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
    file.value = null;
  }
});

const optionsFn = (fecha) => {
  return fecha >= '2022/01/01' && fecha <= hoy.value
}

const getHoy = () => {
  let today = new Date();
  let year = today.getFullYear();
  let month = today.getMonth() + 1;
  if (month < 10) {
    month = "0" + month;
  }
  let day = today.getDate();
  date.value = year + "/" + month + "/" + day;
  hoy.value = date.value
};

const events = ref([]);

const getEvents = () => {
  diariosTaxi.value.forEach((element) => {
    events.value.push(element.dia.replaceAll("-", "/"));
  });
};

const getDiarios = async() => {
  if (diario.value[0]) {
    await taxiStore.get_ingresos_diarios();
    taxiStore.diarios.forEach((element) => {
      diariosTaxi.value = [];
      if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
        diariosTaxi.value.push(element);
      }
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
  file.value = null;
};

const validarVarios = () => {
  //console.log(typeof varios.value,varios.value,varios.value[0])
  if (varios.value) {
    //console.log('existe')
    for (var i = 0; i < varios.value.length; i++) {
      //console.log(varios.value[i])
      if (varios.value[i] != '') { //Las dos están escritas
        if (i % 2 == 0) {
          console.log('concepto', varios.value[i])
          if (isNaN(varios.value[i]) || varios.value[i] > 1000000) {
            return true } //es un número menor de un millón
        } else {
          console.log('cantidad', varios.value[i])
          if (varios.value[i].length > 25 || varios.value[i].length < 3) {
            return true } //es un string entre 2 y 24 letras
        }
      } else return true
    }
  }
  return false;
}

const saveState = computed(() => {
  if (!total_efectivo.value ||
    total_efectivo.value < 0 ||
    total_efectivo.value > 1000000 ||
    isNaN(total_efectivo.value) ||
    !total_tpv.value ||
    total_tpv.value < 0 ||
    total_tpv.value > 1000000 ||
    isNaN(total_tpv.value) ||
    !total_apps.value ||
    total_apps.value < 0 ||
    total_apps.value > 1000000 ||
    isNaN(total_apps.value) ||
    validarVarios()
    //file.value == null
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
  let array
  if (varios.value != null) {
    if (varios.value[0] == 'null') {
      array = []
    } else { array = Object.values(varios.value); }
    const found = array.lastIndexOf("") == -1;
    if (found) {
      array.push("");
      array.push("");
      varios.value = array;
    }
  }
}

const subir = async() => {
  await taxiStore.refresToken();
  if (taxiStore.access_token) {
    let axiosConfig = {
      headers: {
        Authorization: `Bearer ${taxiStore.access_token}`,
      },
    };
    var formData = new FormData();
    formData.append("dia", date.value.replaceAll("/", "-"));
    formData.append("total_efectivo", total_efectivo.value);
    formData.append("total_apps", total_apps.value);
    formData.append("total_tpv", total_tpv.value);

    if (varios.value != null) {
      if (varios.value[0] != 'null') {
        for (let i = 0; i < varios.value.length; i++) {
          const element = varios.value[i];
          formData.append("vario", element);
        }

      }
    } else formData.append("vario", null);
    formData.append("taxista_id", taxiStore.user.id);
    if (file.value) { formData.append("imagen", file.value) }
    if (events.value.indexOf(date.value) != -1) {
      console.log('PUT')
      await api
        .put(`/ingreso_diario/${diario.value[0].id}/`, formData, axiosConfig)
        .then((res) => {
          imagen.value = res.data.imagen;
          date.value = res.data.dia.replaceAll("-", "/");
          getEvents();
          file.value = null;
        })
        .catch((err) => {
          console.log(err.response);
        });
    } else {
      console.log('POST')

      await api
        .post(`/ingreso_diario/create/`, formData, axiosConfig)
        .then((res) => {
          imagen.value = res.data.imagen;
          date.value = res.data.dia.replaceAll("-", "/");
          diariosTaxi.value.push(res.data);
          getEvents();
          file.value = null;
        })
        .catch((err) => {
          console.log(err.response);
        });
    }

  }
};

onMounted(async() => {
  await taxiStore.get_ingresos_diarios();
  taxiStore.diarios.forEach((element) => {
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      diariosTaxi.value.push(element);
    }
  });
  getHoy();
  diariosTaxi.value.sort(function(a, b) {
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
