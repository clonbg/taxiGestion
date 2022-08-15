<template>
  <q-item clickable :to="to">
    <q-item-section v-if="icon" avatar>
      <q-icon color="black" :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label class="text-black">{{ title }}</q-item-label>
      <q-item-label caption>{{ caption }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

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
  },
});
</script>
