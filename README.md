# Simple Damage Tracker

This is a very basic damage tracking system put together to track losses related to my ebay business.
It allows for entry of return/damaged product losses as well as general warehouse losses.

## Vue Version

The new [web based version](https://fir-damage-tracker.firebaseapp.com/) is written in Vue and uses Firebase's Auth and Firestore for user authentication and data storage.

It is designed to allow anyone with access to the website to add a damage report by using the big pink plus.

All other access is restricted to admin users.

## Current Features:

- Freely add damage reports for both eBay orders and warehouse damages
- Automatically tally and display current damages on home page.
- Display damage reports in sortable table with easy access to edit and delete functions
- Able to add/edit/delete reasons for the following
  - Reasons for logging the damage report
  - eBay accounts to track order damages to
  - Product categories and associated costs
- Download all logged damages as csv file
- Able to upload csv file from Python Version

[![Image of demo page](/images/damages.jpg)](https://fir-damage-tracker.firebaseapp.com/)

[A live demo can be viewed here! ](https://fir-damage-tracker.firebaseapp.com/)

Admin login:

- username: test@test.com
- password: test1234

## Python Version

The original version was written with Python 3 and is still available.
