<template>
  <div class="nav-bar">

    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <router-link :to="{ name: 'Index' }">
          <a class="navbar-item">Damage Tracker</a>
        </router-link>
      </div>
      <div class="navbar-menu">
        <div class="navbar-end">
          <router-link :to="{ name: 'AddDamages' }">
            <button class="button is-large is-primary">
            <span class="icon is-large">
              <i class="mdi mdi-plus mdi-48px"></i>  <!-- bell -->
            </span>
            </button>
          </router-link>
        </div>
      </div>
    </nav>
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
.nav-bar nav {
  padding: 10px 20px;
  background-color: #1976d2;
}
.nav-bar button {
  border-radius: 50px;
}
.nav-bar .navbar-brand a {
  color: white;
  font-size: 1.4em;
}
</style>
