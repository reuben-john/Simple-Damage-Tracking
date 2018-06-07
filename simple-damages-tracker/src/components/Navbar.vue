<template>
  <div class="nav-bar">
    <nav class="navbar" role="navigation" aria-label="dropdown navigation">
      <div class="nav-brand navbar-item">
        <router-link :to="{ name: 'Index' }">
          <a class="nav-title">Damage Tracker</a>
        </router-link>
      </div>

      <div class="navbar-end">
        <a href="" class="navbar-item">
          <router-link :to="{ name: 'AddDamages' }">
            <h3 class="navbar-end">Add</h3>
          </router-link>
        </a>
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
  padding: 0 20px;
}
</style>
