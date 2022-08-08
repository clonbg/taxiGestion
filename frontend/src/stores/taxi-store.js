import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "src/boot/axios";

export const useTaxiStore = defineStore("counter", () => {
  const token = ref("token");

  const newToken = async () => {
    try {
      const res = await api.post("/djoser/jwt/create/", {
        email: "clonbg@gmail.com",
        password: "m4nu3l",
      });
      token.value = res.data.access;
    } catch (err) {
      console.log(err);
    }
  };
  return {
    token,
    newToken
  }
});
