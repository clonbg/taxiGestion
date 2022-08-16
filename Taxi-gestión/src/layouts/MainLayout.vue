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
          {{ taxiStore.user ? taxiStore.user[0].nombre : "" }}
          {{ taxiStore.user ? taxiStore.user[0].apellidos : "" }}
        </q-toolbar-title>

        <div>
          <q-btn
            color="green"
            class="q-mx-md"
            @click="taxiStore.access()"
            v-if="!taxiStore.access_token"
          >
            Login
          </q-btn>
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
import { ref } from "vue";
import EssentialLink from "components/EssentialLink.vue";
import { useTaxiStore } from "../stores/taxi-store";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { onMounted } from "vue";

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
    icon: "attach_money",
    to: "/diario",
  },
  {
    title: "Ingresos semanales",
    caption: "cada semana",
    icon: "attach_moneyattach_money",
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
    to: "http://127.0.0.1:8000/admin/",
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
    message: "Está seguro de abandonar la sesión?",
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
