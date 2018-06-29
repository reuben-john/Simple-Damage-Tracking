<template>

        <v-card>
          <v-card-title primary-title>
            <v-flex>
              <h2>Damage Reasons</h2>
              <li v-for="(reason, index) in damageReasons" :key="index"> {{reason.department}}: {{reason.reasons}}</li>
            </v-flex>
          </v-card-title>
          <v-card-text>

          </v-card-text>
        </v-card>

</template>

<script>
export default {
  name: 'EditDamageReasons',
  props: ['damageReasons'],
  data() {
    return {}
  }
}
</script>

<style>
</style>
