<template>
  <q-item
    clickable
    @click="leer(to)"
    v-if="
      (!admin && (taxiStore.user ? !taxiStore.user.is_superuser : false)) ||
      (admin && (taxiStore.user ? taxiStore.user.is_superuser : false)) ||
      to == '/'
    "
  >
    <q-item-section v-if="icon" avatar class="q-mb-xs">
      <q-icon
        :color="router.currentRoute.value.path == to ? 'green' : 'black'"
        :name="icon"
      />
    </q-item-section>
    <q-item-section>
      <q-item-label
        :class="
          router.currentRoute.value.path == to ? 'text-green' : 'text-black'
        "
        >{{ title }}</q-item-label
      >
      <q-item-label caption>{{ caption }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";
import { useRouter } from "vue-router";
import { openURL } from "quasar";
import { useTaxiStore } from "../stores/taxi-store";

export default defineComponent({
  name: "EssentialLink",
  props: {
    title: {
      type: String,
      required: true,
    },

    caption: {
      type: String,
      default: "",
    },

    to: {
      type: String,
      default: "#",
    },

    icon: {
      type: String,
      default: "",
    },

    link: {
      type: String,
      default: "",
    },
    admin: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    const router = useRouter();
    const taxiStore = useTaxiStore();

    return { router, taxiStore };
  },
  methods: {
    leer(to) {
      if (to[0] == "/") {
        this.router.push(to);
      } else {
        openURL(to);
      }
    },
  },
});
</script>
