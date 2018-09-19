<template>
  <v-layout column>
    <v-flex xs12 sm6>
      <v-card>
        <v-container fluid grid-list-md>
          <v-layout row wrap>
            <v-flex xs-6>
              <v-card>
                <v-form @submit.prevent="updateEbayAccount">
                <v-card-title primary-title>
                    <v-flex align-center>
                    <h2>Edit or Delete Ebay Account</h2>
                    </v-flex>
                </v-card-title>
                  <v-container fill-height fluid pa-2 >
                    <v-layout fill-height>
                      <v-flex xs12 sm4>
                        <v-select
                          :items="ebayAccounts.accounts"
                          v-model="account"
                          label="Ebay Account to Edit"
                          single-line
                          required
                        ></v-select>
                      </v-flex>
                      <v-flex xs12 sm4 v-if="account">
                        <v-text-field
                          required v-model="updatedAccount" label="Update Account">
                        </v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>

                <v-card-actions>
                  <v-layout row wrap justify-center>
                    <v-flex xs2 >
                      <v-btn color="success" v-if="updatedAccount"
                        type="submit"
                        >
                        Update
                      </v-btn>
                    </v-flex>
                    <v-flex xs2 >
                      <v-btn color="error" v-if="account"
                        @click="deleteAccount"
                        >
                        Delete
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </v-card-actions>
                </v-form>
              </v-card>
            </v-flex>

            <!-- Second card -->
            <v-flex xs-6>
              <v-card>
                <v-form @submit.prevent="addEbayAccount">
                <v-card-title primary-title>
                    <v-flex align-center>
                    <h2>Add New Ebay Account</h2>
                    </v-flex>
                </v-card-title>

                  <v-container fill-height fluid pa-2 >
                    <v-layout fill-height>
                      <v-flex xs12 sm4>
                        <v-text-field
                          required v-model="newAccount" label="Add New Ebay Account">
                        </v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>

                <v-card-actions>
                  <v-layout row wrap justify-center>
                    <v-flex xs2 >
                      <v-btn color="info" v-if="newAccount"
                        type="submit"
                        >
                        Add
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </v-card-actions>
                </v-form>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import db from '@/firebase/init'

export default {
  name: 'EditEbayAccounts',
  props: ['ebayAccounts'],
  data() {
    return {
      account: '',
      updatedAccount: '',
      newAccount: '',
      newAccountCurrentName: ''
    }
  },
  methods: {
    clearfields() {
      // Clears fields after saving changes
      this.account = ''
      this.updatedAccount = ''
      this.newAccount = ''
    },
    getKeyByValue(object, value) {
      // Gets key based on selected ebay account
      // This is used to ensure we are accessing the correct firestore doc
      return Object.keys(object).find(key => object[key].ebayAccount === value)
    },
    updateEbayAccount() {
      // Update ebay account with new name
      let accounts = this.ebayAccounts.accounts
      let id = this.getKeyByValue(this.ebayAccounts, this.account)
      let index = accounts.indexOf(this.account)
      this.ebayAccounts.accounts[index] = this.updatedAccount

      this.updateDatabase(this.updatedAccount, id)
      this.clearfields()
    },
    addEbayAccount() {
      // Adds new ebay account

      let accounts = this.ebayAccounts.accounts
      // Generate new id
      let id = this.newAccount.toLowerCase()
      id = id.replace(' ', '_')
      this.ebayAccounts.accounts.push(this.newAccount)

      this.updateDatabase(this.newAccount, id)
      this.clearfields()
    },
    updateDatabase(account, id) {
      // Propogate changes to firestore

      console.log(this.updatedAccount, id)
      // update database
      db
        .collection('ebayAccounts')
        .doc(id)
        .set(
          {
            ebayAccount: account
          },
          { merge: true }
        )
        .then(console.log('Updated'))
        .catch(err => console.log)
    },
    deleteFromDatabase(id) {
      // delete item from database
      db
        .collection('ebayAccounts')
        .doc(id)
        .delete()
        .then(console.log('Deleted'))
        .catch(err => console.log)
    },
    deleteAccount() {
      // Deletes ebay account

      let accounts = this.ebayAccounts.accounts
      let id = this.getKeyByValue(this.ebayAccounts, this.account)
      let index = accounts.indexOf(this.account)

      confirm('Are you sure you want to delete this item?') &&
        (accounts.splice(index, 1), (this.ebayAccounts.accounts = accounts), this.deleteFromDatabase(id))

      this.clearfields()
    }
  }
}
</script>

<style>
</style>
