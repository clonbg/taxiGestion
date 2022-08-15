<template>
  <div class="login">
    <h3 class="title">Gestión de taxis</h3>
    <form class="form" @submit.prevent="login()">
      <q-input
        class="q-mb-md"
        dark
        standout
        v-model="email"
        label="Correo
      electrónico"
        type="email"
        stack-label
        :rules="[
          (val) =>
            (val && /^[^@]+@[^@]+\.[a-zA-Z]{2,}$/.test(val)) ||
            'El correo no es correcto',
        ]"
      />

      <q-input
        dark
        standout
        v-model="password"
        label="Contraseña"
        type="password"
        stack-label
        :rules="[
          (val) => (val && val.length > 3) || 'Password mínimo 4 caracteres',
        ]"
      />
      <q-btn class="form-submit" type="submit">Login</q-btn>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useTaxiStore } from "../stores/taxi-store";
import { useRouter } from "vue-router";

const router = useRouter();

const taxiStore = useTaxiStore();

const email = ref(null);
const password = ref(null);

const login = async () => {
  if (email.value && password.value) {
    await taxiStore.access(email.value, password.value);
    if (taxiStore.access_token) {
      router.push("/");
      email.value = "";
      password.value = "";
    }
  }
};
</script>

<style lang="scss" scoped>
.login {
  padding: 5rem;
}
.title {
  text-align: center;
}
.form {
  margin: 3rem auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 20%;
  min-width: 350px;
  max-width: 100%;
  background: rgba(19, 35, 47, 0.9);
  border-radius: 5px;
  padding: 40px;
  box-shadow: 0 4px 10px 4px rgba(0, 0, 0, 0.3);
}

.form-submit {
  background: #1ab188;
  border: none;
  color: black;
  margin-top: 3rem;
  padding: 1rem 1rem;
  cursor: pointer;
  transition: background 0.2s;
  &:hover {
    background: #0b9185;
  }
}
</style>
