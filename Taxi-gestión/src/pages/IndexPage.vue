<template>
  <q-page padding>
    <q-btn @click="access()" class="q-ma-md">Ingresar</q-btn>
    <q-btn @click="refresToken()" class="q-ma-md">Refresh</q-btn>
    <q-btn @click="listaUsuarios()" class="q-ma-md">Usuarios</q-btn>
    <p>ACCESS: {{ access_token }}</p>

    <p></p>
  </q-page>
</template>

<script setup>
import { api } from "../boot/axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

const $router = useRouter();
const access_token = ref(null);

const access = () => {
  api
    .post("/djoser/jwt/create/", {
      email: "clonbg@gmail.com",
      password: "m4nu3l",
    })
    .then((res) => {
      access_token.value = res.data.access;
      localStorage.setItem("tmp_taxi_access_token", Date.now());
      localStorage.setItem("taxi_refresh_token", res.data.refresh);
      localStorage.setItem("tmp_taxi_refresh_token", Date.now());
    })
    .catch((err) => {
      console.log(err.request);
    });
};
const refresToken = async () => {
  if (
    access_token.value === null ||
    access_token.value == "" ||
    access_token.value == undefined ||
    localStorage.getItem("tmp_taxi_access_token") === null ||
    localStorage.getItem("tmp_taxi_access_token") == "" ||
    Date.now() - localStorage.getItem("tmp_taxi_access_token") > 14 * 60 * 1000
  ) {
    console.log("no es valido el access token");
    if (
      localStorage.getItem("taxi_refresh_token") === null ||
      localStorage.getItem("taxi_refresh_token") == "" ||
      localStorage.getItem("tmp_taxi_refresh_token") === null ||
      localStorage.getItem("tmp_taxi_refresh_token") == "" ||
      Date.now() - localStorage.getItem("tmp_taxi_refresh_token") >
        7 * 24 * 60 * 60 * 1000 - 60000
    ) {
      console.log("no es válido el refresh token");
      $router.push("/login");
    } else {
      const res = await api.post("/djoser/jwt/refresh/", {
        refresh: localStorage.getItem("taxi_refresh_token"),
      });
      access_token.value = res.data.access;
      localStorage.setItem("tmp_taxi_access_token", Date.now());
    }
  }
};
const listaUsuarios = async () => {
  await refresToken();
  let axiosConfig = {
    headers: {
      Authorization: `Bearer ${access_token.value}`,
    },
  };
  api
    .get("/taxistas/registro/", axiosConfig)
    .then((res) => {
      console.log(res.data);
    })
    .catch((err) => {
      console.log(err.request);
    });
};
</script>
