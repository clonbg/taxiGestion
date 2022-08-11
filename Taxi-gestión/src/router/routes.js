
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'diario', component: () => import('pages/IngresoDiario.vue') },
      { path: 'semanal', component: () => import('pages/IngresoSemanal.vue') },
      { path: 'graficas', component: () => import('src/pages/GraficasPage.vue') },

    ]
  },

  {
    path: '/login',
    component: () => import('pages/LoginPage.vue')
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
