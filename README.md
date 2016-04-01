# Coursera Downloader
- to answer [a question in quora](https://www.quora.com/Is-there-a-way-to-mass-download-the-materials-from-a-Coursera-course/answer/Jansen-Simanullang?share=1):
```
    Is there a way to mass download the materials from a Coursera course?
```


## Download all videos in all weeks of all lesson in one specified course.

- downloading from the old 'http://class.coursera.org' is easy since:
    - it is a simple html and can be parsed with html parser;
    - all links to the course material is provided in one page url;
    - you can use many popular software like 'DownThemAll' to download all the materials you wish to download;
    - there are many solutions already provided in github.com for this purpose;

- downloading from the new 'https://www.coursera.org' however is harder since:
    - it is javascript rendered and must be parsed using a browser engine, meaning: the html elements you want to parse may not be visible until you view it in a browser;
    - links to the course materials are spread within many page urls;
    - you will get tired of downloading after 144 urls;

- this compiled python gives solution to download all videos, subtitles and transcripts in:
```
    https://www.coursera.org/
```
- usage:
```
    python www-coursera-downloader.pyc
```
- You will be prompted to supply user (email) and password for your Coursera account;
```
-----------------------------------------------------------------------

-------------------- WELCOME TO COURSERA DOWNLOADER -------------------
please kindly support my daily sustenance: vera.verum.veritas@gmail.com

-----------------------------------------------------------------------


one time setup user and password

Enter your e-mail address: vera.verum.veritas@gmail.com
vera.verum.veritas@gmail.com

Enter your Coursera password: somesecretwords
***************

User and password has been saved to coursera.pass file.
Please delete the file if you want to change your credentials.

```
- Your credentials are encrypted and then saved locally into a file named coursera.pass placed in the same folder of this script.

- You will be prompted to select the course:
```
-----------------------------------------------------------------------

-------------------- WELCOME TO COURSERA DOWNLOADER -------------------
please kindly support my daily sustenance: vera.verum.veritas@gmail.com

-----------------------------------------------------------------------


Getting courses list...
Welcome to Coursera!

There are 13 courses available

[1] Machine Learning: Regression
[2] Machine Learning Foundations: A Case Study Approach
[3] Using Databases with Python
[4] Using Python to Access Web Data
[5] R Programming
[6] Practical Predictive Analytics: Models and Methods
[7] Machine Learning: Recommender Systems & Dimensionality Reduction
[8] Machine Learning: Clustering & Retrieval
[9] Machine Learning: Classification
[10] The Data ScientistÔÇÖs Toolbox
[11] Computational Investing, Part I
[12] Machine Learning for Data Analysis
[13] Practical Machine Learning

[  ] Please pick course number!
```
- bot will crawl all the lesson in all weeks of your selected course;
- it then will download all the videos, subtitles and transcripts in your selected course.

## Requirements
- Python packages requirements:
```
    Crypto, os, re, sys, splinter, selenium, time, urllib2
```

- Javascript package requirement:
```
    phantomjs
```

- Download PhantomJS from phantomjs.org:
```
    http://phantomjs.org/download.html
```

- You may want to use [phantomjsInstaller.sh](phantomjsInstaller.sh) within this repository.

- for windows users please check recommended packages [here](windows.md).

if you find it useful please donate: vera.verum.veritas@gmail.com, I am looking for a new job.
