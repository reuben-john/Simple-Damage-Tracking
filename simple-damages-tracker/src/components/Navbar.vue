<template>
  <div class="nav-bar">
      <v-toolbar color="primary">
      <v-toolbar-title>
        <router-link :to="{ name: 'Index' }">
          <span class="white--text">Damage Tracker</span>
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn fab top right color="pink white--text" :to="{ name: 'AddDamages' }">
          <v-icon>add</v-icon>
        </v-btn>
      </v-toolbar-items>
      </v-toolbar>
  </div>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {}
  }
}
</script>

<style>
</style>
