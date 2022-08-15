import { route } from "quasar/wrappers";
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import routes from "./routes";
import { useTaxiStore } from "../stores/taxi-store";

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === "history"
    ? createWebHistory
    : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  Router.beforeEach(async (to, from, next) => {
    const protegida = to.meta.auth;
    const taxiStore = useTaxiStore();

    if (protegida) {
      await taxiStore.refresToken();
      if (taxiStore.access_token) {
        if (taxiStore.user != null) {
          if (!taxiStore.user[0].is_superuser && to.meta.admin) {
            return next('/')
          }
        }
        return next(); //Si es protegida y existe el access_token
      }
      return next("/login"); //Si es protegida y NO existe el access_token
    }
    if (to.path == "/login") {
      if (taxiStore.access_token) {
        return next("/"); //Si es la página de login y existe el access_token
      }
    }
    next();
  });

  return Router;
});
