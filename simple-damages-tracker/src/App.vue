<template>
  <div id="app">
    <v-app>
    <Navbar></Navbar>

    <router-view/>
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
