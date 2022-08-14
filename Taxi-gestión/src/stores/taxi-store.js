import { defineStore } from "pinia";
import { api } from "../boot/axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { Notify } from "quasar";

export const useTaxiStore = defineStore("taxi", () => {
  const router = useRouter();
  const access_token = ref(null);
  const user = ref(null);
  const emailUsuario = ref(null);

  const access = async (email, password) => {
    const res = await api
      .post("/djoser/jwt/create/", {
        email: email,
        password: password,
      })
      .then((res) => {
        Notify.create({
          type: "positive",
          message: "Ha sido logueado correctamente",
        });
        emailUsuario.value = email;
        access_token.value = res.data.access;
        localStorage.setItem("tmp_taxi_access_token", Date.now());
        localStorage.setItem("taxi_refresh_token", res.data.refresh);
        localStorage.setItem("tmp_taxi_refresh_token", Date.now());
      })
      .catch((err) => {
        Notify.create({
          type: "negative",
          message: "Algo ha fallado¡¡",
        });
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
      Date.now() - localStorage.getItem("tmp_taxi_access_token") >
        14 * 60 * 1000
    ) {
      console.log("no es valido el access token");
      access_token.value = null;
      if (
        localStorage.getItem("taxi_refresh_token") === null ||
        localStorage.getItem("taxi_refresh_token") == "" ||
        localStorage.getItem("tmp_taxi_refresh_token") === null ||
        localStorage.getItem("tmp_taxi_refresh_token") == "" ||
        Date.now() - localStorage.getItem("tmp_taxi_refresh_token") >
          7 * 24 * 60 * 60 * 1000 - 60000
      ) {
        console.log("no es válido el refresh token");
      } else {
        const res = await api.post("/djoser/jwt/refresh/", {
          refresh: localStorage.getItem("taxi_refresh_token"),
        });
        access_token.value = res.data.access;
        localStorage.setItem("tmp_taxi_access_token", Date.now());
      }
    }
  };
  const logout = async () => {
    access_token.value = null;
    localStorage.removeItem("tmp_taxi_access_token");
    localStorage.removeItem("tmp_taxi_refresh_token");
    localStorage.removeItem("taxi_refresh_token");
  };
  return {
    access_token,
    user,
    emailUsuario,
    access,
    refresToken,
    logout,
  };
});
