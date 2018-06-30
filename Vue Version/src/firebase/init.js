import firebase from 'firebase'
import firestore from 'firebase/firestore'

// Initialize Firebase
var config = {
  apiKey: 'AIzaSyDwAAGh-7XFYkuxa5L3_PFPMBUBbynk71g',
  authDomain: 'fir-damage-tracker.firebaseapp.com',
  databaseURL: 'https://fir-damage-tracker.firebaseio.com',
  projectId: 'fir-damage-tracker',
  storageBucket: '',
  messagingSenderId: '184323133734'
}
const firebaseApp = firebase.initializeApp(config)
firebaseApp.firestore().settings({ timestampsInSnapshots: true })

// export firestore database
export default firebaseApp.firestore()
