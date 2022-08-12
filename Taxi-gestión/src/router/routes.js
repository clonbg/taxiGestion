const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("pages/IndexPage.vue"),
        meta: { auth: true },
      },
      {
        path: "diario",
        component: () => import("pages/IngresoDiario.vue"),
        meta: { auth: true },
      },
      {
        path: "semanal",
        component: () => import("pages/IngresoSemanal.vue"),
        meta: { auth: true },
      },
      {
        path: "graficas",
        component: () => import("src/pages/GraficasPage.vue"),
        meta: { auth: true },
      },
    ],
  },

  {
    path: "/login",
    component: () => import("pages/LoginPage.vue"),
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
