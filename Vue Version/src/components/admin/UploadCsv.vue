<template>
        <v-card>
          <v-card-text>
            <v-layout row wrap justify-space-around>
              <v-flex xs12 sm8 v-if="csvFile">
                <v-data-table
                  :headers="csvFile.headers"
                  :items="csvFile.csvData"
                  hide-actions
                  class="elevation-1"
                  >
                  <template slot="items" slot-scope="props">
                    <td class="text-xs-left">{{ props.item[csvFile.headers[0].value] }}</td>
                    <td class="justify-center layout px-0">
                      <v-btn icon class="mx-0" @click="editItem(props.item)">
                        <v-icon color="teal">edit</v-icon>
                      </v-btn>
                      <v-btn icon class="mx-0" @click="deleteItem(props.item)">
                        <v-icon color="pink">delete</v-icon>
                      </v-btn>
                    </td>
                  </template>
                </v-data-table>
              </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-actions>
            <v-layout row wrap justify-center>
              <v-flex>
                <input type="file" accept=".csv" @change="uploadCsvFile">
                <!-- <upload-btn color="success" accept=".csv" @change="onFileChange" title="Upload CSV File"></upload-btn> -->
              </v-flex>
            </v-layout>
          </v-card-actions>
        </v-card>

</template>

<script>
import db from '@/firebase/init'
import papaparse from 'papaparse'
import UploadButton from 'vuetify-upload-button'

export default {
  name: 'UploadCsv',
  components: {
    'upload-btn': UploadButton
  },
  data() {
    return {
      csvFile: null
    }
  },
  methods: {
    uploadCsvFile(e) {
      this.csvFile = {}
      let files = e.target.files || e.dataTransfer.files
      if (!files.length) return
      let vm = this
      // Parse csv file
      papaparse.parse(files[0], {
        complete: function(results) {
          vm.parseFile(results.data)
          // this.csvFile = results.data
        }
      })
    },
    parseFile(file) {
      let headers = file[0]
      this.csvFile.headers = []
      for (let i = 0; i < headers.length; i++) {
        this.csvFile.headers.push({
          text: headers[i],
          value: headers[i]
        })
      }

      let data = file.slice(1)
      let newData = []

      for (let line = 0; line < data.length; line++) {
        let newFile = {}
        for (let i = 0; i < headers.length; i++) {
          newFile[headers[i]] = data[line][i]
        }
        newData.push(newFile)
      }
      this.csvFile.csvData = newData
      console.log(this.csvFile)
    },
    convertNumbers() {
      let report = Object.assign(this.item)

      // Convert string to numbers for different fields before adding to database
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
