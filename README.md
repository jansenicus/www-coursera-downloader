# FEATURES
- download quizzes and practice quizzes.
- download all video lectures;
- download vtt subtitles;
- automatic conversion of vtt to srt format;
- read html readings and save to html file;
- creation of m3u playlist.


# PREVIEW
Click [here](http://nbviewer.jupyter.org/github/jansenicus/www-coursera-downloader/blob/master/WWW-COURSERA-DOWNLOADER.ipynb) to preview the Notebook

# REQUIREMENTS:
```
python3
jupyter notebook
```

# Coursera Downloader
- to answer [several similar questions in quora](https://www.quora.com/Is-there-a-way-to-mass-download-the-materials-from-a-Coursera-course/answer/Jansen-Simanullang?share=1):
```
    Is there a way to mass download the materials from a Coursera course?
    
    How can I download all the video lectures of a coursera course in one go?
    
    Are there any ways to batch download the complete course videos on coursera new platform?
    
    How do I write a Python script that automatically downloads all the videos of the course from Coursera?
    
    Ashish Kedia: How can I write a Script in Python to mass download all course videos from Coursera new platform and name them by lecture title?
    
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
    jupyter notebook
```


