# OfflineAlberts
  This script was made to make a local copy of questions and answers of review material on Albert.io. Very useful for studying on the road/when you have no wifi/saving questions past when your subscription ends.

  You will need an active Albert.io subscription to be able to use this, but since this saves a local copy, you will have the review material after your subscription expires.

 The script uses selenium to automate the collection of screenshots of the review questions and explainations. The basic premise is to have selenium log in and collect the review topic links. The script then goes through these links and screenshots the questions. These screenshots are saved to the /images directory.

