<template>
  <div class="nav-bar">
      <v-toolbar color="primary">
      <v-toolbar-title>
        <router-link :to="{ name: 'Index' }">
          <span class="white--text ml-2">Damage Tracker</span>
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn v-if="user" flat class="white--text" :to="{ name: 'ViewAdmin' }">Admin</v-btn>
        <v-btn v-if="!user" flat class="white--text mr-4" :to="{ name: 'Login' }">Login</v-btn>
        <v-btn v-if="user" flat class="white--text mr-4" @click="logout">Logout</v-btn>
        <v-btn class="add" fab top right large color="pink white--text mt-2" :to="{ name: 'AddDamages' }">
          <v-icon>add</v-icon>
        </v-btn>
      </v-toolbar-items>
      </v-toolbar>
  </div>
</template>

<script>
import firebase from 'firebase/app'
import 'firebase/auth'

export default {
  name: 'Navbar',
  data() {
    return {
      user: null
    }
  },
  methods: {
    logout() {
      // Logs user out
      firebase
        .auth()
        .signOut()
        .then(() => {
          this.$router.push({ name: 'Login' })
        })
    }
  },
  created() {
    // Checks if user is logged in
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
.nav-bar {
  margin-bottom: 30px;
}
</style>
