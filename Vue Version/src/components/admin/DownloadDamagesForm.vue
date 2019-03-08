<template>
  <v-card>
    <v-card-text>
      <h2>Download Damages Report</h2>
    </v-card-text>
    <v-card-actions>
      <v-layout row wrap justify-center>
        <v-flex xs12 sm2>
          <v-select :items="years" v-model="CSVYear" label="Year" single-line required></v-select>
          <v-btn
            v-if="CSVYear"
            color="purple darken-1 white--text"
            @click="downloadDamagesReport()"
          >Download Damage Report</v-btn>
        </v-flex>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<script>
import db from '@/firebase/init'
import moment from 'moment'
import papaparse from 'papaparse'

export default {
  name: 'DownloadDamagesForm',
  props: ['years'],
  data() {
    return {
      CSVYear: null,
      CSVReport: null
    }
  },
  methods: {
    downloadDamagesReport() {
      // this.downloadPDF()
      console.log(this.CSVYear)
      this.downloadCSV()
    },
    // downloadPDF() {
    //   // Create pdf file for damage report
    //   let doc = new jsPDF()
    //   doc.text(['Kendy Corporation', 'Damage Report'], 110, 10, {
    //     align: 'center'
    //   })
    //   doc.text([])
    //   doc.save('damages.pdf')
    // },
    downloadCSV() {
      // Creates CSV file of all damage reports

      // Clears CSVreport
      this.CSVReport = []
      // fetch damages data from firestore
      db.collection('damages')
        .where('damageDept', '==', 'order')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            let report = doc.data()
            if (moment(report.timestamp).format('YYYY') == this.CSVYear) {
              report.date = moment(report.timestamp).format('LL')
              this.CSVReport.push(report)
            }
          })
          // saves firestore data as csv - Must be inside [] for file-saver to work
          let csv = [papaparse.unparse(this.CSVReport, { download: true })]
          var FileSaver = require('file-saver')
          var blob = new Blob(csv, { type: 'text/plain;charset=utf-8' })
          FileSaver.saveAs(blob, this.CSVYear + '-damages.csv')
        })
        .catch(err => console.log(err))
    }
  }
}
</script>

<style>
</style>
