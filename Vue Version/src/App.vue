<template>
  <div id="app">
    <v-app>
    <Navbar></Navbar>
    <v-content>
      <router-view/>
    </v-content>
    </v-app>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'

export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style>
</style>
