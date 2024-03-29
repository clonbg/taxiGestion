<template>
  <q-page class="flex flex-center q-ma-sm">
    <div class="row float-left" style="margin-right: 15%; width: 15rem">
      <q-date v-model="date" :events="events" today-btn :options="optionsFn" :locale="myLocale" />
    </div>

    <q-form class="form float-right" @submit.prevent="subir()" autocorrect="off" autocapitalize="off" autocomplete="off"
      spellcheck="false" style="width: 30rem">
      <q-img :src="
        `${taxiStore.urlServer}${imagen_semana}` != `${taxiStore.urlServer}`
          ? `${taxiStore.urlServer}${imagen_semana}`
          : ' '
      " class="q-my-xl" :class="{
  zoom:
    `${taxiStore.urlServer}${imagen_semana}` !=
    `${taxiStore.urlServer}`,
}" :ratio="16 / 9">
        <div class="absolute-bottom-right text-subtitle2 cursor-pointer"
          @click="openURL(`${taxiStore.urlServer}${imagen_semana}`)">
          Abrir
        </div>
        <template v-slot:error>
          <div class="absolute-full flex flex-center bg-negative text-white">
            No se puede cargar la imagen
          </div>
        </template>
      </q-img>
      <q-file v-model="file" :label="
        events.indexOf(date) == -1
          ? 'Inserte la imagen (5Mb Max)'
          : 'Puede cambiar la imagen (5Mb Max)'
      " filled :rules="[
  (val) =>
    (events.indexOf(date) == -1 ? val : true) ||
    'La imagen es obligatoria',
]" max-file-size="5242880" @rejected="onRejected" :filter="validarFile">
        <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>
      </q-file>
      <div class="row">
        <div class="col-6">
          <q-input ref="inicioRef" class="q-mt-md" label="día inicial" filled v-model="dia_inicio" mask="##/##/####"
            :error="!validaFecha">
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-date v-model="dia_inicio" mask="DD/MM/YYYY" :options="optionsImputDate">
                    <div class="row items-center justify-end">
                      <q-btn v-close-popup label="Close" color="primary" flat />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </div>
        <div class="col-6">
          <q-input ref="finRef" class="q-ml-sm q-mt-md" label="día final" filled v-model="dia_fin" mask="##/##/####"
            :error="!validaFecha">
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-date v-model="dia_fin" mask="DD/MM/YYYY" :options="optionsImputDate">
                    <div class="row items-center justify-end">
                      <q-btn v-close-popup label="Close" color="primary" flat />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input standout v-model="total_efectivo_semana" label="Efectivo" dense :rules="[
            (val) =>
              (val !== '' &&
                val >= 0 &&
                !isNaN(val) &&
                val <= 1000000 &&
                dosDecimales(val)) ||
              'Valor no válido',
          ]" />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input standout v-model="total_tpv_semana" label="TPV" dense :rules="[
            (val) =>
              (val !== '' &&
                val >= 0 &&
                !isNaN(val) &&
                val <= 1000000 &&
                dosDecimales(val)) ||
              'Valor no válido',
          ]" />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input standout v-model="total_apps_semana" label="Apps" dense :rules="[
            (val) =>
              (val !== '' &&
                val >= 0 &&
                !isNaN(val) &&
                val <= 1000000 &&
                dosDecimales(val)) ||
              'Valor no válido',
          ]" />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input standout v-model="varios_semana" label="Varios" dense :rules="[
            (val) =>
              (val !== '' &&
                val >= -1000000 &&
                !Number.isNaN(val) &&
                val <= 1000000 &&
                dosDecimales(val)) ||
              'Valor no válido',
          ]" />
        </div>
      </div>
      <q-btn class="form-submit" type="submit" :disable="saveState" :color="saveState ? 'red' : 'green'"
        :loading="loadingGuardar[0]">Guardar</q-btn>
      <q-btn class="form-submit q-ml-md q-my-md" @click="getSemanal()" color="primary">Cancelar</q-btn>
      <q-btn v-if="semanal?.length == 1 ? true : false" class="form-submit q-ml-md q-my-md" @click="confirmaBorrar()"
        color="negative" :loading="loadingBorrar[0]">Eliminar</q-btn>
    </q-form>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, computed, ref, watchEffect } from "vue";
import moment from "moment";
import { useQuasar, Notify, openURL } from "quasar";
import { api } from "../boot/axios";

const taxiStore = useTaxiStore();
const semanalesTaxi = ref([]);
const semanal = ref(null);
const imagen_semana = ref(null);
const date = ref(null);
const hoy = ref(null);
const events = ref([]);
const file = ref(null);
const dia_inicio = ref(null);
const inicioRef = ref(null);
const dia_fin = ref(null);
const finRef = ref(null);
const total_efectivo_semana = ref(null);
const total_tpv_semana = ref(null);
const total_apps_semana = ref(null);
const varios_semana = ref(null);

const $q = useQuasar();

const onRejected = (rejectedEntries) => {
  file.value = null;
  Notify.create({
    type: "negative",
    message: `${rejectedEntries.length} archivo(s) no han pasado la validación`,
  });
};

const validarFile = (archivo) => {
  console.log(archivo);
  return archivo.filter(
    (file) => file.type == "image/jpeg" || file.type == "image/png"
  );
};

const myLocale = {
  days: "Domingo_Lunes_Martes_Miércoles_Jueves_Viernes_Sábado".split("_"),
  daysShort: "Dom_Lun_Mar_Mié_Jue_Vie_Sáb".split("_"),
  months:
    "Enero_Febrero_Marzo_Abril_Mayo_Junio_Julio_Agosto_Septiembre_Octubre_Noviembre_Diciembre".split(
      "_"
    ),
  monthsShort: "Ene_Feb_Mar_Abr_May_Jun_Jul_Ago_Sep_Oct_Nov_Dic".split("_"),
  firstDayOfWeek: 1, // 0-6, 0 - Sunday, 1 Monday, ...
  format24h: true,
  pluralDay: "dias",
};

const getHoy = () => {
  let today = new Date();
  let year = today.getFullYear();
  let month = today.getMonth() + 1;
  if (month < 10) {
    month = "0" + month;
  }
  let day = today.getDate();
  if (day < 10) {
    day = "0" + day;
  }
  date.value = year + "/" + month + "/" + day;
  hoy.value = date.value;
};

const getEvents = () => {
  events.value = [];
  semanalesTaxi.value.forEach((element) => {
    let fecha1 = moment(element.dia_inicio);
    let fecha2 = moment(element.dia_fin);
    for (; fecha1 <= fecha2;) {
      events.value.push(fecha1.format("YYYY/MM/DD"));
      fecha1.add(1, "day");
    }
  });
};

const optionsFn = (fecha) => {
  return fecha >= "2022/01/01" && fecha <= hoy.value;
};

const optionsImputDate = (fecha) => {
  let today = new Date(hoy.value);
  let todayMOne = moment(today);
  todayMOne.add(1, "day");
  let inicio = semanalesTaxi.value.filter(
    (element) => element.id == semanal.value[0]?.id
  );
  events.value.sort();
  let posI = events.value.lastIndexOf(
    inicio[0]?.dia_inicio.replaceAll("-", "/")
  );
  let posF = events.value.lastIndexOf(inicio[0]?.dia_fin.replaceAll("-", "/"));
  if (posI != -1 || posF != -1) {
    return (
      fecha >
      (events.value[posI - 1] ? events.value[posI - 1] : "2022/01/01") &&
      fecha <
      (events.value[posF + 1]
        ? events.value[posF + 1]
        : todayMOne.format("YYYY/MM/DD"))
    );
  } else {
    let newArray = events.value.slice();
    let buscar = newArray.lastIndexOf(date.value);
    if (buscar == -1) {
      newArray.push(date.value);
    }
    newArray.sort();
    let pos = newArray.lastIndexOf(date.value);
    return (
      fecha > (pos == 0 ? "2022/01/01" : newArray[pos - 1]) &&
      fecha <
      (pos == newArray.length - 1
        ? todayMOne.format("YYYY/MM/DD")
        : newArray[pos + 1])
    );
  }
};

watchEffect(() => {
  if (date.value) {
    semanal.value = semanalesTaxi.value.filter(
      (dia) =>
        moment(dia.dia_inicio) <= new Date(date.value) &&
        moment(dia.dia_fin) >= new Date(date.value)
    );
    if (semanal.value[0]) {
      imagen_semana.value = semanal.value[0].imagen_semana;
      dia_inicio.value = moment(semanal.value[0].dia_inicio).format(
        "DD/MM/YYYY"
      );
      dia_fin.value = moment(semanal.value[0].dia_fin).format("DD/MM/YYYY");
      total_efectivo_semana.value = semanal.value[0].total_efectivo_semana;
      total_tpv_semana.value = semanal.value[0].total_tpv_semana;
      total_apps_semana.value = semanal.value[0].total_apps_semana;
      varios_semana.value = semanal.value[0].varios_semana;
    } else {
      imagen_semana.value = "";
      dia_inicio.value = "";
      dia_fin.value = "";
      total_efectivo_semana.value = "";
      total_tpv_semana.value = "";
      total_apps_semana.value = "";
      varios_semana.value = "";
    }
    file.value = null;
  }
});

const validaFecha = computed(() => {
  if (dia_inicio.value && dia_fin.value) {
    let fecha = new Date(dia_inicio.value.split("/").reverse().join("/"));
    let fechaDeInicio = moment(fecha);
    fecha = new Date(dia_fin.value.split("/").reverse().join("/"));
    let fechaFinal = moment(fecha);
    if (
      fechaDeInicio.isValid() &&
      fechaFinal.isValid() &&
      dia_fin.value.length == 10 &&
      dia_inicio.value.length == 10 &&
      fechaDeInicio.diff(fechaFinal) <= 0
    ) {
      return true;
    }
    return false;
  }
  return false;
});

const dosDecimales = (num) => {
  let pos = num?.toString().lastIndexOf(".");
  if (num && pos != -1) {
    let cantDecimales = num.toString().length - pos;
    if (cantDecimales == 3 || cantDecimales == 2) {
      return true;
    }
  }
  if (pos == -1) {
    return true;
  }
  return false;
};

const saveState = computed(() => {
  if (
    total_efectivo_semana.value === "" ||
    total_efectivo_semana.value < 0 ||
    total_efectivo_semana.value > 1000000 ||
    !dosDecimales(total_efectivo_semana.value) ||
    isNaN(total_efectivo_semana.value) ||
    total_tpv_semana.value === "" ||
    total_tpv_semana.value < 0 ||
    total_tpv_semana.value > 1000000 ||
    !dosDecimales(total_tpv_semana.value) ||
    isNaN(total_tpv_semana.value) ||
    total_apps_semana.value === "" ||
    total_apps_semana.value < 0 ||
    total_apps_semana.value > 1000000 ||
    !dosDecimales(total_apps_semana.value) ||
    isNaN(total_apps_semana.value) ||
    varios_semana.value === "" ||
    varios_semana.value < -1000000 ||
    varios_semana.value > 1000000 ||
    !dosDecimales(varios_semana.value) ||
    isNaN(varios_semana.value) ||
    (!semanal.value[0]?.id && file.value == null) ||
    !validaFecha.value
  ) {
    return true;
  }
  return false;
});

// const nuevo = () => {
//   imagen_semana.value = "";
//   dia_inicio.value = "";
//   dia_fin.value = "";
//   total_efectivo_semana.value = "";
//   total_tpv_semana.value = "";
//   total_apps_semana.value = "";
//   varios_semana.value = "";
// };

const eliminarSemanal = async () => {
  await taxiStore.refresToken();
  if (taxiStore.access_token) {
    let axiosConfig = {
      headers: {
        Authorization: `Bearer ${taxiStore.access_token}`,
      },
    };
    let pos = semanalesTaxi.value.lastIndexOf(semanal.value[0]);
    if (pos != -1) {
      await api
        .delete(`/ingreso_semanal/${semanal.value[0].id}/`, axiosConfig)
        .then(() => { })
        .catch((err) => {
          console.log(err.response);
        });
      semanalesTaxi.value.splice(pos, 1);
    }
  }
};

const loadingBorrar = ref([false, false, false, false, false, false]);
const simulateProgressBorrar = (number) => {
  // we set loading state
  loadingBorrar.value[number] = true;
  // simulate a delay
  setTimeout(() => {
    // we're done, we reset loading state
    loadingBorrar.value[number] = false;
    eliminarSemanal();
    events.value = [];
    semanalesTaxi.value.forEach((element) => {
      if (element.id != semanal.value[0].id) {
        let fecha1 = moment(element.dia_inicio);
        let fecha2 = moment(element.dia_fin);
        for (; fecha1 <= fecha2;) {
          events.value.push(fecha1.format("YYYY/MM/DD"));
          fecha1.add(1, "day");
        }
      }
    });
    Notify.create({
      type: "warning",
      message: "Ha sido eliminado correctamente",
    });
  }, 3000);
};

const loadingGuardar = ref([false, false, false, false, false, false]);
const simulateProgressGuardar = (number, res) => {
  // we set loading state
  loadingGuardar.value[number] = true;

  // simulate a delay
  setTimeout(() => {
    // we're done, we reset loading state
    loadingGuardar.value[number] = false;
    if (res.data.id == semanal.value[0]?.id) {
      imagen_semana.value = res.data.imagen_semana;
      dia_inicio.value = res.data.dia_inicio.replaceAll("-", "/");
      dia_fin.value = res.data.dia_fin.replaceAll("-", "/");
      let pos = semanalesTaxi.value.filter((t) => t.id == semanal.value[0].id);
      pos = semanalesTaxi.value.lastIndexOf(pos[0]);
      semanalesTaxi.value.splice(pos, 1);
      semanalesTaxi.value.push(res.data);
      getEvents();
      file.value = null;
    } else {
      imagen_semana.value = res.data.imagen;
      semanalesTaxi.value.push(res.data);
      getEvents();
      file.value = null;
    }
    Notify.create({
      type: "positive",
      message: "Ha sido guardado correctamente",
    });
  }, 3000);
};

const confirmaBorrar = () => {
  $q.dialog({
    title: "Cuidado",
    message: `¿Está seguro de eliminar del día ${dia_inicio.value} al ${dia_fin.value}?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    simulateProgressBorrar(0);
  });
};

const getSemanal = async () => {
  if (semanal.value[0]) {
    await taxiStore.get_ingresos_semanales();
    semanalesTaxi.value = [];
    taxiStore.semanales.forEach((element) => {
      if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
        semanalesTaxi.value.push(element);
      }
    });
    semanal.value = semanalesTaxi.value.filter(
      (dia) =>
        moment(dia.dia_inicio) <= new Date(date.value) &&
        moment(dia.dia_fin) >= new Date(date.value)
    );
  } else {
    imagen_semana.value = "";
    dia_inicio.value = "";
    dia_fin.value = "";
    total_efectivo_semana.value = "";
    total_tpv_semana.value = "";
    total_apps_semana.value = "";
    varios_semana.value = "";
  }
  file.value = null;
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
    formData.append(
      "dia_inicio",
      dia_inicio.value.split("/").reverse().join("-")
    );
    formData.append("dia_fin", dia_fin.value.split("/").reverse().join("-"));
    if (file.value) {
      formData.append("imagen_semana", file.value);
    }
    formData.append("total_efectivo_semana", total_efectivo_semana.value);
    formData.append("total_apps_semana", total_apps_semana.value);
    formData.append("total_tpv_semana", total_tpv_semana.value);
    formData.append("varios_semana", varios_semana.value);

    formData.append("taxista_id", taxiStore.user.id);
    //Función para ver si el id existe
    if (semanal.value[0]?.id) {
      await api
        .put(`/ingreso_semanal/${semanal.value[0].id}/`, formData, axiosConfig)
        .then((res) => {
          simulateProgressGuardar(0, res);
        })
        .catch((err) => {
          console.log(err.response);
        });
    } else {
      await api
        .post(`/ingreso_semanal/create/`, formData, axiosConfig)
        .then((res) => {
          simulateProgressGuardar(0, res);
        })
        .catch((err) => {
          console.log(err.response);
        });
    }
  }
};

onMounted(async () => {
  await taxiStore.get_ingresos_semanales();
  taxiStore.semanales.forEach((element) => {
    if (element.taxista?.email == localStorage.getItem("email_taxi_user")) {
      semanalesTaxi.value.push(element);
    }
  });
  getHoy();
  semanalesTaxi.value.sort(function (a, b) {
    return new Date(b.dia_fin) - new Date(a.dia_fin);
  });
  getEvents();
  semanal.value = semanalesTaxi.value.filter(
    (dia) =>
      moment(dia.dia_inicio) <= new Date(date.value) &&
      moment(dia.dia_fin) >= new Date(date.value)
  );
});
</script>

<style scoped>
.zoom {
  transition: transform 0.2s;
}

.zoom:hover {
  transform: scale(1.2);
}
</style>
