import { defineStore } from "pinia";
import { api } from "../boot/axios";
import { ref } from "vue";
import { Notify } from "quasar";

export const useTaxiStore = defineStore("taxi", () => {
  const urlServer = ref("http://localhost:8000");
  const access_token = ref(null);
  const user = ref(null);
  const diarios = ref(null);
  const semanales = ref(null)
  const letrero = { nombre: ref(null), apellidos: ref(null) };
  const listaUsuarios = ref(null);

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
        localStorage.setItem("email_taxi_user", email);
        access_token.value = res.data.access;
        localStorage.setItem("tmp_taxi_access_token", Date.now());
        localStorage.setItem("taxi_refresh_token", res.data.refresh);
        localStorage.setItem("tmp_taxi_refresh_token", Date.now());
      })
      .catch((err) => {
        Notify.create({
          type: "negative",
          message: JSON.stringify(err.response.data.detail),
        });
        console.log(err.response.data.detail);
      });
    usuario();
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
  const usuario = async () => {
    await refresToken();
    if (access_token.value) {
      let axiosConfig = {
        headers: {
          Authorization: `Bearer ${access_token.value}`,
        },
      };
      await api
        .get("/taxistas/registro/", axiosConfig)
        .then((res) => {
          const tmp = res.data.filter(
            (user) => user.email == localStorage.getItem("email_taxi_user")
          );
          user.value = tmp[0];
          localStorage.setItem("id_taxi_user", user.value.id);
          letrero.nombre = user.value.nombre;
          letrero.apellidos = user.value.apellidos;
          listaUsuarios.value = res.data;
        })
        .catch((err) => {
          console.log(err.request);
        });
    }
  };

  const get_ingresos_diarios = async () => {
    await refresToken();
    if (access_token.value) {
      let axiosConfig = {
        headers: {
          Authorization: `Bearer ${access_token.value}`,
        },
      };
      await api
        .get("/ingreso_diario/create/", axiosConfig)
        .then((res) => {
          diarios.value = res.data;
        })
        .catch((err) => {
          console.log(err.request);
        });
    }
  };

    const get_ingresos_semanales = async () => {
    await refresToken();
    if (access_token.value) {
      let axiosConfig = {
        headers: {
          Authorization: `Bearer ${access_token.value}`,
        },
      };
      await api
        .get("/ingreso_semanal/create/", axiosConfig)
        .then((res) => {
          console.log(res.data)
          semanales.value = res.data;
        })
        .catch((err) => {
          console.log(err.request);
        });
    }
  };

  const logout = async () => {
    access_token.value = null;
    localStorage.removeItem("tmp_taxi_access_token");
    localStorage.removeItem("tmp_taxi_refresh_token");
    localStorage.removeItem("taxi_refresh_token");
    localStorage.removeItem("email_taxi_user");
    localStorage.removeItem("id_taxi_user");
  };
  return {
    access_token,
    user,
    urlServer,
    letrero,
    listaUsuarios,
    diarios,
    semanales,
    access,
    refresToken,
    logout,
    usuario,
    get_ingresos_diarios,
    get_ingresos_semanales
  };
});
