<template>
  <q-page class="flex flex-center">
    <div>{{taxiStore.token}}</div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import {useTaxiStore} from '../stores/taxi-store'



export default defineComponent({
  name: 'IndexPage',
  setup() {
    const taxiStore = useTaxiStore()
    return {
      taxiStore
    }
  },
  created(){
    //this.taxiStore.newToken()
  }
})
</script>
