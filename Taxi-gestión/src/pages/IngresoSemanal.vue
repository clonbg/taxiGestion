<template>
  <q-page class="flex flex-center">
    <q-date
      v-model="date"
      :events="events"
      class="float-left"
      style="margin-right: 15%"
      today-btn
      :options="optionsFn"
      :locale="myLocale"
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
        :src="
          `${taxiStore.urlServer}${imagen_semana}` != `${taxiStore.urlServer}`
            ? `${taxiStore.urlServer}${imagen_semana}`
            : ' '
        "
        class="q-my-xl"
        :class="{
          zoom:
            `${taxiStore.urlServer}${imagen_semana}` !=
            `${taxiStore.urlServer}`,
        }"
        :ratio="16 / 9"
        ><div
          class="absolute-bottom-right text-subtitle2 cursor-pointer"
          @click="openURL(`${taxiStore.urlServer}${imagen_semana}`)"
        >
          Abrir
        </div>
        <template v-slot:error>
          <div class="absolute-full flex flex-center bg-negative text-white">
            No se puede cargar la imagen
          </div>
        </template>
      </q-img>
      <q-file
        v-model="file"
        :label="
          events.indexOf(date) == -1
            ? 'Inserte la imagen'
            : 'Puede cambiar la imagen'
        "
        filled
        :rules="[
          (val) =>
            (events.indexOf(date) == -1 ? val : true) ||
            'La imagen es obligatoria',
        ]"
      >
        <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>
      </q-file>
      <div class="row">
        <div class="col-6">
          <q-input
            label="día inicial"
            filled
            v-model="dia_inicio"
            mask="##/##/####"
            :rules="[(val) => fechaValida(val) || 'La fecha no es válida']"
          >
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy
                  cover
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-date v-model="dia_inicio" mask="DD/MM/YYYY">
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
          <q-input
            class="q-ml-sm"
            label="día final"
            filled
            v-model="dia_fin"
            mask="##/##/####"
            :rules="[(val) => fechaValida(val) || 'La fecha no es válida']"
          >
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy
                  cover
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-date v-model="dia_fin" mask="DD/MM/YYYY">
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
          <q-input
            standout
            v-model="total_efectivo_semana"
            label="Efectivo"
            dense
            :rules="[
              (val) =>
                (val &&
                  val >= 0 &&
                  !isNaN(val) &&
                  val <= 1000000 &&
                  dosDecimales(val)) ||
                'Valor no válido',
            ]"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input
            standout
            v-model="total_tpv_semana"
            label="TPV"
            dense
            :rules="[
              (val) =>
                (val &&
                  val >= 0 &&
                  !isNaN(val) &&
                  val <= 1000000 &&
                  dosDecimales(val)) ||
                'Valor no válido',
            ]"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input
            standout
            v-model="total_apps_semana"
            label="Apps"
            dense
            :rules="[
              (val) =>
                (val &&
                  val >= 0 &&
                  !isNaN(val) &&
                  val <= 1000000 &&
                  dosDecimales(val)) ||
                'Valor no válido',
            ]"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <q-input
            standout
            v-model="varios_semana"
            label="Varios"
            dense
            :rules="[
              (val) =>
                (val &&
                  val >= -1000000 &&
                  !Number.isNaN(val) &&
                  val <= 1000000 &&
                  dosDecimales(val)) ||
                'Valor no válido',
            ]"
          />
        </div>
      </div>
    </q-form>
  </q-page>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { onMounted, computed, ref, watchEffect } from "vue";
import moment from "moment";
import { useQuasar, Notify, openURL } from "quasar";

const taxiStore = useTaxiStore();
const semanalesTaxi = ref([]);
const semanal = ref(null);
const imagen_semana = ref(null);
const date = ref(null);
const hoy = ref(null);
const events = ref([]);
const file = ref(null);
const dia_inicio = ref(null);
const dia_fin = ref(null);
const total_efectivo_semana = ref(null);
const total_tpv_semana = ref(null);
const total_apps_semana = ref(null);
const varios_semana = ref(null);

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
  semanalesTaxi.value.forEach((element) => {
    let fecha1 = moment(element.dia_inicio);
    let fecha2 = moment(element.dia_fin);
    for (; fecha1 <= fecha2; ) {
      events.value.push(fecha1.format("YYYY/MM/DD"));
      fecha1.add(1, "day");
    }
  });
};

const optionsFn = (fecha) => {
  return fecha >= "2022/01/01" && fecha <= hoy.value;
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
      dia_inicio.value = moment(semanalesTaxi.value[0].dia_inicio).format(
        "DD/MM/YYYY"
      );
      dia_fin.value = moment(semanalesTaxi.value[0].dia_fin).format(
        "DD/MM/YYYY"
      );
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
  }
});

const fechaValida = (f) => {
  if (moment(f.split("/").reverse().join("-")).isValid() && f.length == 10) {
    return true;
  }
  return false;
};

const dosDecimales = (num) => {
  let pos = num.toString().lastIndexOf(".");
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
