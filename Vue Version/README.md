# Simple Damages Tracker

##Demo Version

You may view the [app live here](https://fir-damage-tracker.firebaseapp.com/)

Demo login is:

- username: test@test.com
- password: test1234

> A Vue app for tracking shipping and warehouse damages

This app is built using Vue. It uses Vuetify for a css framework and vue-router to handle routing. It uses firestore for a database.

## TODOs

- [ ] Add tests
- [ ] Add better comments
- [ ] Add form validation to ensure forms are filled out fully with correct info
- [ ] Add an animation that shows the new tally being added to the total before updating
- [ ] Add transition/loading animations
- [ ] Add form feedback messages to show something has happened
- [ ] Add upload form to upload csv file from python version into web version
- [ ] Add export option to download data as csv file
- [ ] Make total damage tracker only show current year's damages (Jan 1 - Dec 31)
- [ ] Allow data to be viewed by year on the damages views
- [ ] Add archive feature to remove old reports

## Build Setup

```bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
