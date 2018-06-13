<template>
  <v-container class="view-admin" text-xs-center fill-height>
    <v-layout row wrap align-center justify-center>
      <v-flex xs12 sm10>
        <v-card>
          <v-card-title primary-title>
            <v-flex>
              <h2>Admin Options</h2>
            </v-flex>
          </v-card-title>
          <v-card-text>
            <v-layout row wrap>
              <v-flex xs12 sm6>
              <v-btn color="purple darken-1 white--text" >View Damage Reasons</v-btn>
            </v-flex>
            <v-flex xs12 sm6>
              <v-btn color="purple darken-1 white--text">View Product Costs</v-btn>
            </v-flex>
            </v-layout>

          </v-card-text>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'ViewAdmin',
  data() {
    return {}
  }
}
</script>
