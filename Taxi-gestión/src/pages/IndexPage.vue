<template>
  <q-page padding>
    <q-btn @click="access()" class="q-ma-md">Ingresar</q-btn>
    <q-btn @click="refresToken()" class="q-ma-md">Refresh</q-btn>
    <q-btn @click="listaUsuarios()" class="q-ma-md">Usuarios</q-btn>
    <p>ACCESS: {{ access_token }}</p>

    <p></p>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { api } from "../boot/axios";
import { ref } from "vue";

export default defineComponent({
  setup() {
    const access_token = ref(null);

    //access()
    //refresToken();
    //listaUsuarios()

    return {
      access_token,
    };
  },
  methods: {
    access() {
      api
        .post("/djoser/jwt/create/", {
          email: "clonbg@gmail.com",
          password: "m4nu3l",
        })
        .then((res) => {
          this.access_token = res.data.access;
          localStorage.setItem("tmp_taxi_access_token", Date.now());
          localStorage.setItem("taxi_refresh_token", res.data.refresh);
          localStorage.setItem("tmp_taxi_refresh_token", Date.now());
        })
        .catch((err) => {
          console.log(err.request);
        });
    },
    async refresToken() {
      if (
        this.access_token === null ||
        this.access_token == "" ||
        this.access_token == undefined ||
        localStorage.getItem("tmp_taxi_access_token") === null ||
        localStorage.getItem("tmp_taxi_access_token") == "" ||
        Date.now() - localStorage.getItem("tmp_taxi_access_token") >
          14 * 60 * 1000
      ) {
        console.log("no es valido el access token");
        console.log(
          localStorage.getItem("taxi_refresh_token"),
          localStorage.getItem("tmp_taxi_refresh_token")
        );
        if (
          localStorage.getItem("taxi_refresh_token") === null ||
          localStorage.getItem("taxi_refresh_token") == "" ||
          localStorage.getItem("tmp_taxi_refresh_token") === null ||
          localStorage.getItem("tmp_taxi_refresh_token") == "" ||
          Date.now() - localStorage.getItem("tmp_taxi_refresh_token") >
            7 * 24 * 60 * 60 * 1000 - 60000
        ) {
          console.log("no es válido el refresh token");
          console.log("Deberiamos volver al login");
        } else {
          await api
            .post("/djoser/jwt/refresh/", {
              refresh: localStorage.getItem("taxi_refresh_token"),
            })
            .then((res) => {
              this.access_token = res.data.access;
              localStorage.setItem("tmp_taxi_access_token", Date.now());
            })
            .catch((err) => {
              console.log(err.request);
            });
        }
      }
    },
    async listaUsuarios() {
      await this.refresToken();
      let axiosConfig = {
        headers: {
          Authorization: `Bearer ${this.access_token}`,
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
    },
  },
});
</script>
