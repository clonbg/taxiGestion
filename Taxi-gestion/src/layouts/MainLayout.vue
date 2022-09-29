<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          {{ taxiStore.letrero.nombre + " " + taxiStore.letrero.apellidos }}
        </q-toolbar-title>

        <div>
          <span class="q-mr-sm text-yellow">{{ ruta }}</span>
          <q-btn
            icon="mdi-location-exit"
            color="red"
            @click="confirmaLogout"
          ></q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="bg-grey-4">
      <q-list>
        <q-item-label header> Secciones </q-item-label>
        <EssentialLink
          v-for="link in essentialLink"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, computed } from "vue";
import EssentialLink from "components/EssentialLink.vue";
import { useTaxiStore } from "../stores/taxi-store";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { onMounted } from "vue";
let ruta = computed(() => {
  if (router.currentRoute.value.fullPath == "/") {
    return "Perfil de usuario";
  } else if (router.currentRoute.value.fullPath == "/diario") {
    return "Ingresos diarios";
  } else if (router.currentRoute.value.fullPath == "/semanal") {
    return "Ingresos semanales";
  } else if (router.currentRoute.value.fullPath == "/graficas") {
    return "Gráficos y comparativas";
  } else return "";
});
const router = useRouter();

const taxiStore = useTaxiStore();

const $q = useQuasar();

const essentialLink = [
  {
    title: "Perfil de usuario",
    caption: localStorage.getItem("email_taxi_user"),
    icon: "person",
    to: "/",
  },
  {
    title: "Ingresos diarios",
    caption: "cada día",
    icon: "$",
    to: "/diario",
  },
  {
    title: "Ingresos semanales",
    caption: "cada semana",
    icon: "$$",
    to: "/semanal",
  },
  {
    title: "Gráficas",
    caption: "comparativas",
    icon: "insert_chart_outlined",
    to: "/graficas",
    admin: true,
  },
  {
    title: "Base de datos",
    caption: "Base de datos",
    icon: "storage",
    to: `${taxiStore.urlServer}/api/admin/`,
    admin: true,
  },
];

const leftDrawerOpen = ref(false);

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value;
};
const logout = async () => {
  taxiStore.logout();
  router.push("/login");
  $q.notify({
    type: "info",
    message: "Ha salido de la aplicación",
  });
};
const confirmaLogout = () => {
  $q.dialog({
    title: "Cuidado",
    message: "¿Está seguro de abandonar la sesión?",
    cancel: true,
    persistent: true,
  }).onOk(() => {
    logout();
  });
};

onMounted: {
  taxiStore.usuario();
}
</script>
