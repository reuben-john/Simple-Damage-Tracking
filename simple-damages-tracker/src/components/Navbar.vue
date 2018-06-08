<template>
  <div class="nav-bar">

    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <router-link :to="{ name: 'Index' }">
          <a class="navbar-item"  color="white--text">Damage Tracker</a>
        </router-link>
      </div>
      <div class="navbar-menu">
        <div class="navbar-end">
          <router-link :to="{ name: 'AddDamages' }">
            <h3>Add</h3>
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
}
</style>
