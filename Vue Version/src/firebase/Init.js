import firebase from 'firebase'
import firestore from 'firebase/firestore'

// Initialize Firebase
var config = {
  apiKey: 'AIzaSyAwO2MpPYHeBKFKCBFnKM68dGpyUmzEiB8',
  authDomain: 'simple-damage-tracking.firebaseapp.com',
  databaseURL: 'https://simple-damage-tracking.firebaseio.com',
  projectId: 'simple-damage-tracking',
  storageBucket: 'simple-damage-tracking.appspot.com',
  messagingSenderId: '108907129773'
}
const firebaseApp = firebase.initializeApp(config)
firebaseApp.firestore().settings({ timestampsInSnapshots: true })

// export firestore database
export default firebaseApp.firestore()
