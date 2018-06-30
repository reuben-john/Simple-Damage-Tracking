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
        <v-btn flat class="white--text" :to="{ name: 'ViewAdmin' }">Admin</v-btn>
        <v-btn flat class="white--text" :to="{ name: 'Login' }">Login</v-btn>
        <v-btn class="add" fab top right large color="pink white--text" :to="{ name: 'AddDamages' }">
          <v-icon>add</v-icon>
        </v-btn>
      </v-toolbar-items>
      </v-toolbar>
  </div>
</template>

<script>
import firebase from 'firebase'

export default {
  name: 'Navbar',
  data() {
    return {
      user: null
    }
  },
  methods: {
    logout() {
      firebase
        .auth()
        .signOut()
        .then(() => {
          this.$router.push({ name: 'Login' })
        })
    }
  },
  created() {
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        this.user = user
      } else {
        this.user = null
      }
    })
  }
}
</script>

<style>
.nav-bar .add {
  margin-top: 1em;
}
</style>
