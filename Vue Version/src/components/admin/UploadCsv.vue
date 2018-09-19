<template>
        <v-card>
          <v-card-text>
            <h2>Upload CSV File</h2>
          </v-card-text>
          <v-card-actions>
            <v-layout row wrap justify-center>
              <v-flex xs12 sm2>
                <v-select
                  :items="damageReasons.departments"
                  v-model="department"
                  label="Choose Department"
                  single-line
                  required
                ></v-select>
              </v-flex>
              <v-flex xs12 sm4 v-if="department">
                <input type="file" accept=".csv" @change="uploadCsvFile">
                <!-- <upload-btn color="success" accept=".csv" @change="onFileChange" title="Upload CSV File"></upload-btn> -->
              </v-flex>

            </v-layout>
          </v-card-actions>
          <div><h3 v-if="feedback" class="red--text pb-3">{{ feedback }}</h3></div>
        </v-card>

</template>

<script>
import db from '@/firebase/init'
import papaparse from 'papaparse'
import UploadButton from 'vuetify-upload-button'
import moment from 'moment'

export default {
  name: 'UploadCsv',
  components: {
    'upload-btn': UploadButton
  },
  props: ['damageReasons'],
  data() {
    return {
      csvFile: null,
      department: '',
      feedback: '',

      // Table headers
      headers: {
        warehouse: ['timestamp', 'itemType', 'itemCost', 'itemsLost', 'reasonLost', 'damageDept'],
        order: [
          'timestamp',
          'orderNumber',
          'orderTotal',
          'shippingCost',
          'shippingLost',
          'itemType',
          'itemCost',
          'itemsLost',
          'reasonLost',
          'damageDept',
          'ebayAccount'
        ]
      }
    }
  },
  methods: {
    logDamages() {
      // Saves damage report

      for (let report in this.csvFile) {
        // Send damage report to database
        db
          .collection('damages')
          .add(this.csvFile[report])
          .then(console.log('Added', this.csvFile[report]))
          .catch(err => console.log(err))
      }
    },
    formatWarehouseFile(file) {
      // Formats warehouse file to match desired firestore doc format
      // This is for migrating data from python version to Vue version

      let newFile = []
      for (let line in file) {
        // Rename old damage reasons to new ones
        if (file[line].reasonLost == 'Box loss') {
          file[line].reasonLost = 'Bad Box'
        }

        if (file[line].reasonLost == 'Item loss') {
          file[line].reasonLost = 'Bad Product'
        }

        let updatedFile = {
          timestamp: parseInt(moment(file[line].timestamp, 'MM-DD-YYYY').format('x')),
          itemType: file[line].itemType,
          itemCost: parseFloat(file[line].itemCost),
          itemsLost: parseFloat(file[line].itemsLost),
          reasonLost: file[line].reasonLost,
          damageDept: file[line].damageDept
        }

        newFile.push(updatedFile)
      }

      this.csvFile = newFile
      this.logDamages()
    },
    formatOrderFile(file) {
      // Formats warehouse file to match desired firestore doc format
      // This is for migrating data from python version to Vue version

      let newFile = []
      for (let line in file) {
        // Rename old damage reasons to new ones
        if (file[line].reasonLost == 'Order lost in transit') {
          file[line].reasonLost = 'Lost in Transit'
        }

        if (file[line].reasonLost == 'Returned product') {
          file[line].reasonLost = 'Returned Product'
        }

        let updatedFile = {
          timestamp: parseInt(moment(file[line].timestamp, 'MM-DD-YYYY').format('x')),
          orderNumber: file[line].orderNumber,
          orderTotal: parseFloat(file[line].orderTotal),
          shippingCost: parseFloat(file[line].shippingCost),
          shippingLost: parseFloat(file[line].shippingLost),
          itemType: file[line].itemType,
          itemCost: parseFloat(file[line].itemCost),
          itemsLost: parseFloat(file[line].itemsLost),
          reasonLost: file[line].reasonLost,
          damageDept: file[line].damageDept,
          ebayAccount: file[line].ebayAccount
        }

        newFile.push(updatedFile)
      }

      this.csvFile = newFile
      this.logDamages()
    },
    uploadCsvFile(e) {
      // Allows user to upload CSV file to process
      // This is for migrating data from python version to Vue version

      let files = e.target.files || e.dataTransfer.files
      if (!files.length) return

      let vm = this
      // Parse csv file
      papaparse.parse(files[0], {
        complete: function(results) {
          vm.parseFile(results.data, e)
        }
      })
    },
    parseFile(file, e) {
      // Check if department matches csv data
      // Subtracts 2 for the extra headers that don't exist in the csv file
      let orderLength = this.headers.order.length - 2
      let warehouseLength = this.headers.warehouse.length - 1
      if (
        (this.department == 'order' && file[0].length != orderLength) ||
        (this.department == 'warehouse' && file[0].length != warehouseLength)
      ) {
        this.feedback = "department and csv file don't match. Make sure you are using the correct csv file"
        e.target.value = ''
        return
      } else {
        setTimeout(() => {
          this.feedback = ''
        }, 2000)
      }

      let data = file.slice(1)
      let newData = []

      for (let line = 0; line < data.length; line++) {
        let newFile = {}
        for (let i = 0; i < this.headers[this.department].length; i++) {
          newFile[this.headers[this.department][i]] = data[line][i]
        }
        newFile.damageDept = this.department
        newFile.ebayAccount = 'Test Store'
        newData.push(newFile)
      }

      if (this.department == 'order') {
        this.formatOrderFile(newData)
      } else if (this.department == 'warehouse') {
        this.formatWarehouseFile(newData)
      }
    },
    convertNumbers() {
      // Convert string to numbers for different fields before adding to database

      let report = Object.assign(this.item)

      report = Object.assign(report, {
        boxCost: parseFloat(report.boxCost),
        itemCost: parseFloat(report.itemCost)
      })
      return report
    }
  }
}
</script>

<style>
</style>
