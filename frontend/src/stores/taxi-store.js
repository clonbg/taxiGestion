import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "src/boot/axios";
import { useRouter } from "vue-router";


export const useTaxiStore = defineStore("counter", () => {
  const token_acceso = ref("");
  const token_refresco = ref("");
  const router = useRouter();

  const newToken = async () => {
    await api
      .post("/djoser/jwt/create/", {
        email: "clonbg@gmail.com",
        password: "m4nu3l",
      })
      .then((res) => {
        console.log(res);
        token_acceso.value = res.data.access;
        token_refresco.value = res.data.refresh;
      })
      .catch((err) => {
        console.log(err);
      });
  };
  const verificaToken = async (token) => {
    await api
      .post("/djoser/jwt/verify/", { token: token })
      .then((res) => {console.log(res)})
      .catch((err) => {
        router.push('/login')
        console.log(err.request);
      });
  };
  newToken();
  return {
    token_acceso,
    token_refresco,
    newToken,
    verificaToken
  };
});
