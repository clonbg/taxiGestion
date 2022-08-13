<template>
  <div class="login">
    <h3 class="title">Página de Login</h3>
    <form action class="form">
      <label class="form-label" for="#email">Email:</label>
      <input
        class="form-input"
        type="email"
        id="email"
        required
        placeholder="Email"
      />
      <label class="form-label" for="#password">Password:</label>
      <input
        class="form-input"
        type="password"
        id="password"
        placeholder="Password"
      />
      <q-btn class="form-submit" placeholder="Login" @click="login()"
        >Login</q-btn
      >
    </form>
  </div>
</template>

<script setup>
import { useTaxiStore } from "../stores/taxi-store";
import { useRouter } from "vue-router";

const router = useRouter();

const taxiStore = useTaxiStore();
const login = async () => {
  await taxiStore.access();
  if (taxiStore.access_token) {
    router.push("/");
  }
};
</script>

<style lang="scss" scoped>
.login {
  padding: 2rem;
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
.form-label {
  margin-top: 2rem;
  color: white;
  margin-bottom: 0.5rem;
  &:first-of-type {
    margin-top: 0rem;
  }
}
.form-input {
  padding: 10px 15px;
  background: none;
  background-image: none;
  border: 1px solid white;
  color: white;
  &:focus {
    outline: 0;
    border-color: #1ab188;
  }
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
