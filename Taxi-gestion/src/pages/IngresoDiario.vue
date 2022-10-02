<template>
  <q-page class="flex flex-center">
    <div class="row float-left" style="margin-right: 15%; width: 15rem">
      <q-date
        v-model="date"
        :events="events"
        today-btn
        :options="optionsFn"
        :locale="myLocale"
      />
      <q-input
        disable
        filled
        class="q-mt-md"
        :label="`Sueldo de ${
          date ? myLocale.months[date?.substring(5, 7) - 1].toLowerCase() : ''
        }`"
        v-model="sueldo"
        suffix="Euros"
      />
    </div>
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
          `${taxiStore.urlServer}${imagen}` != `${taxiStore.urlServer}`
            ? `${taxiStore.urlServer}${imagen}`
            : ' '
        "
        class="q-my-xl"
        :class="{
          zoom: `${taxiStore.urlServer}${imagen}` != `${taxiStore.urlServer}`,
        }"
        :ratio="16 / 9"
        ><div
          class="absolute-bottom-right text-subtitle2 cursor-pointer"
          @click="openURL(`${taxiStore.urlServer}${imagen}`)"
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
            ? 'Inserte la imagen (5Mb Max)'
            : 'Puede cambiar la imagen (5Mb Max)'
        "
        filled
        :rules="[
          (val) =>
            (events.indexOf(date) == -1 ? val : true) ||
            'La imagen es obligatoria',
        ]"
        max-file-size="5242880"
        @rejected="onRejected"
        :filter="validarFile"
      >
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
              (val) =>
                (val !== '' &&
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
            v-model="total_tpv"
            label="TPV"
            dense
            :rules="[
              (val) =>
                (val !== '' &&
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
            v-model="total_apps"
            label="Apps"
            dense
            :rules="[
              (val) =>
                (val !== '' &&
                  val >= 0 &&
                  !isNaN(val) &&
                  val <= 1000000 &&
                  dosDecimales(val)) ||
                'Valor no válido',
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
                    (val &&
                      val >= -1000000 &&
                      !Number.isNaN(val) &&
                      val <= 1000000 &&
                      dosDecimales(val)) ||
                    'Valor no válido',
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
                  (val) =>
                    (val &&
                      val.toString().length >= 3 &&
                      val.toString().length <= 25) ||
                    'Valor no válido',
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
        :loading="loadingGuardar[0]"
        >Guardar</q-btn
      >
      <q-btn
        class="form-submit q-ml-md q-my-md"
        @click="getDiarios()"
        color="primary"
        >Cancelar</q-btn
      >
      <q-btn
        v-if="diario[0] ? true : false"
        class="form-submit q-ml-md q-my-md"
        @click="confirmaBorrar()"
        color="negative"
        :loading="loadingBorrar[0]"
        >Eliminar</q-btn
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
import { useQuasar, Notify, openURL } from "quasar";

const loadingBorrar = ref([false, false, false, false, false, false]);
const loadingGuardar = ref([false, false, false, false, false, false]);

const progress = ref(false);

const simulateProgressBorrar = (number) => {
  // we set loading state
  loadingBorrar.value[number] = true;

  // simulate a delay
  setTimeout(() => {
    // we're done, we reset loading state
    loadingBorrar.value[number] = false;
    events.value = events.value.filter((dia) => dia != date.value);
    eliminarDiario();
    Notify.create({
      type: "warning",
      message: "Ha sido eliminado correctamente",
    });
  }, 3000);
};

const simulateProgressGuardar = (number, res) => {
  // we set loading state
  loadingGuardar.value[number] = true;

  // simulate a delay
  setTimeout(() => {
    // we're done, we reset loading state
    loadingGuardar.value[number] = false;
    if (events.value.indexOf(date.value) != -1) {
      imagen.value = res.data.imagen;
      date.value = res.data.dia.replaceAll("-", "/");
      let item = diariosTaxi.value.filter(
        (item) => item.id == diario.value[0].id
      );
      let pos = diariosTaxi.value.lastIndexOf(item[0]);
      diariosTaxi.value[pos] = res.data;
      file.value = null;
    } else {
      imagen.value = res.data.imagen;
      date.value = res.data.dia.replaceAll("-", "/");
      diariosTaxi.value.push(res.data);
      events.value.push(res.data.dia.replaceAll("-", "/"));
      file.value = null;
    }
    Notify.create({
      type: "positive",
      message: "Ha sido guardado correctamente",
    });
  }, 3000);
};

const $q = useQuasar();

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

const onRejected = (rejectedEntries) => {
  file.value = null;
  Notify.create({
    type: "negative",
    message: `${rejectedEntries.length} archivo(s) no han pasado la validación`,
  });
};

const validarFile = (archivo) => {
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
  file.value = null;
});

const optionsFn = (fecha) => {
  return fecha >= "2022/01/01" && fecha <= hoy.value;
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

const events = ref([]);

const getEvents = () => {
  diariosTaxi.value.forEach((element) => {
    events.value.push(element.dia.replaceAll("-", "/"));
  });
};

const getDiarios = async () => {
  if (events.value.lastIndexOf(date.value) != -1) {
    await taxiStore.get_ingresos_diarios();
    diariosTaxi.value = [];
    taxiStore.diarios.forEach((element) => {
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
  if (varios?.value[0]) {
    for (var i = 0; i < varios.value.length; i++) {
      if (varios.value[i] != "") {
        //Las dos están escritas
        if (i % 2 == 0) {
          if (
            Number.isNaN(varios.value[i]) ||
            varios.value[i] > 1000000 ||
            varios.value[i] < -1000000 ||
            !dosDecimales(varios.value[i])
          ) {
            return true;
          } //es un número menor de un millón
        } else {
          if (varios.value[i].length > 25 || varios.value[i].length < 3) {
            return true;
          } //es un string entre 2 y 24 letras
        }
      } else return true;
    }
  }
  return false;
};

const saveState = computed(() => {
  if (
    !total_efectivo.value === "" ||
    total_efectivo.value < 0 ||
    total_efectivo.value > 1000000 ||
    !dosDecimales(total_efectivo.value) ||
    isNaN(total_efectivo.value) ||
    !total_tpv.value === "" ||
    total_tpv.value < 0 ||
    total_tpv.value > 1000000 ||
    !dosDecimales(total_tpv.value) ||
    isNaN(total_tpv.value) ||
    !total_apps.value === "" ||
    total_apps.value < 0 ||
    total_apps.value > 1000000 ||
    !dosDecimales(total_apps.value) ||
    isNaN(total_apps.value) ||
    validarVarios() ||
    (events.value.indexOf(date.value) == -1 && file.value == null)
  ) {
    return true;
  }
  return false;
});

const borrar = (i) => {
  varios.value.splice(i - 1, 1);
  varios.value.splice(i - 1, 1);
};

const variosMas = () => {
  if (!varios.value) {
    varios.value = [];
  }
  varios.value.push("");
  varios.value.push("");
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

const sueldo = computed(() => {
  if (date.value) {
    let mes = date.value.substring(5, 7);
    let sum = 0;
    diariosTaxi.value.forEach((element) => {
      if (element.dia.substring(5, 7) == mes) {
        if (element.vario) {
          for (var i = 0; i < element.vario.length; i++) {
            if (i % 2 == 0) {
              sum = sum + parseInt(element.vario[i]);
            }
          }
        }
        sum =
          sum + element.total_efectivo + element.total_tpv + element.total_apps;
      }
    });
    return (sum * parseInt(taxiStore.user.sueldo)) / 100;
  }
  //const sueldo = semanalesTaxi.value.filter(item => )
  return 0;
});

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
    formData.append("total_efectivo", total_efectivo.value);
    formData.append("total_apps", total_apps.value);
    formData.append("total_tpv", total_tpv.value);

    for (let i = 0; i < varios.value.length; i++) {
      const element = varios.value[i];
      formData.append("vario", element);
    }

    formData.append("taxista_id", taxiStore.user.id);
    if (file.value) {
      formData.append("imagen", file.value);
    }
    if (events.value.indexOf(date.value) != -1) {
      await api
        .put(`/ingreso_diario/${diario.value[0].id}/`, formData, axiosConfig)
        .then((res) => {
          simulateProgressGuardar(0, res);
        })
        .catch((err) => {
          console.log(err.response);
          Notify.create({
            type: "negative",
            message: "Halgo ha fallado",
          });
        });
    } else {
      await api
        .post(`/ingreso_diario/create/`, formData, axiosConfig)
        .then((res) => {
          simulateProgressGuardar(0, res);
        })
        .catch((err) => {
          console.log(err.response);
          Notify.create({
            type: "negative",
            message: "Halgo ha fallado",
          });
        });
    }
  }
};

const confirmaBorrar = () => {
  if (diario.value[0]) {
    $q.dialog({
      title: "Cuidado",
      message: "¿Está seguro de eliminar este día?",
      cancel: true,
      persistent: true,
    }).onOk(async () => {
      await simulateProgressBorrar(0);
    });
  }
};

const eliminarDiario = async () => {
  await taxiStore.refresToken();
  if (taxiStore.access_token) {
    let axiosConfig = {
      headers: {
        Authorization: `Bearer ${taxiStore.access_token}`,
      },
    };
    let pos = diariosTaxi.value.lastIndexOf(diario.value[0]);
    if (pos != -1) {
      await api
        .delete(`/ingreso_diario/${diario.value[0].id}/`, axiosConfig)
        .then((res) => {})
        .catch((err) => {
          console.log(err.response);
        });
      diariosTaxi.value.splice(pos, 1);
    }
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
.zoom {
  transition: transform 0.2s;
}
.zoom:hover {
  transform: scale(1.2);
}
</style>
