#-*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# CourseraDownloader.py
# (c) Jansen A. Simanullang
# Automated Coursera Downloader
# START: 28.03.2016 18:17
# LAST: 01.04.2016
#---------------------------------------
# usage:
# python CourseraDownloader.py
#
# changes:
# 01.04.2016: Courses list downloaded
#---------------------------------------

from splinter import Browser
from selenium import webdriver
import os, sys, re, time, urllib2, math
from Crypto.Cipher import AES
#--------------------------------
key1 = 'ἀλήθεια,καὶἡζωή'
key2 = 'Ἰησοῦς88'
key1 = key1.decode("utf-8")
key1 = key1.encode("utf-8")
key2 = key2.decode("utf-8")
key2 = key2.encode("utf-8")
headerText = '''
-----------------------------------------------------------------------

-------------------- WELCOME TO COURSERA DOWNLOADER -------------------
please kindly support my daily sustenance: vera.verum.veritas@gmail.com

-----------------------------------------------------------------------

'''
footerText = '''
-----------------------------------------------------------------------
at this time of code writing, I am in need of a new job in new currency
your donation can support my daily sustenance.
paypal: vera.verum.veritas@gmail.com
-----------------------------------------------------------------------
'''
scriptRoot = os.path.dirname(os.path.abspath(__file__)) + os.sep

#--------------------------------


def clearScreen():

	if os.name == 'posix':
		os.system('clear')
	else:
		os.system('cls')

		
		
def adjustStr16(strInput):

	multiples = int(math.ceil(len(strInput)/16.0))

	remainder = len(strInput)%16
	
	quotient = len(strInput)/16

	#print("len: ", len(strInput), "multiples: ", multiples, "remainder: ", remainder, "quotient: ", quotient)
	
	if remainder:
		strInput = strInput.ljust((multiples*16))
	else:
		strInput = strInput
		
	return strInput
	
	

def encrypt(strInput, key1, key2):
	#--------------------------------
	# encrypt(strInput, key1, key2)
	# encrypt a string input with key1 and key2
	#
	key1 = key1.decode("utf-8")
	key1 = key1.encode("utf-8")

	obj = AES.new(key1, AES.MODE_CBC, key2)

	strInput = adjustStr16(strInput)

	encryptedText = obj.encrypt(strInput)

	return encryptedText
	
	

def createPass():

	print "one time setup user and password\n"
	
	email = str(raw_input('Enter your e-mail address: '))
	print email, "\n"
	
	password = str(raw_input('Enter your Coursera password: '))
	print '*'*len(password), "\n"

	strInput = email + ":" + password
	encryptedText = encrypt(strInput, key1, key2)
	fileCreate("coursera.pass",encryptedText)

	return email, password
	
	

def decrypt(strInput, key1, key2):
	#--------------------------------
	# decrypt(strInput, key1, key2)
	# decrypt an encrypted string with key1 and key2
	#

	obj2 = AES.new(key1, AES.MODE_CBC, key2)
	decryptedText = obj2.decrypt(strInput)

	return decryptedText



def fileCreate(strNamaFile, strData):
	#--------------------------------
	# fileCreate(strNamaFile, strData)
	# create a text file
	#
	f = open(strNamaFile, "w")
	f.writelines(str(strData))
	f.close()



def readTextFile(strNamaFile):
	#--------------------------------
	# readTextFile(strNamaFile)
	# read from a text file
	#

	fText = open(strNamaFile)
	strText = ""
					
	for baris in fText.readlines():
		strText += baris
	fText.close()

	return strText

#-------------------------------------

def getUserPass(strPasswordFile):

	strText = readTextFile(strPasswordFile)

	decryptedText = decrypt(strText, key1, key2)
	decryptedText = decryptedText.strip()

	email = decryptedText.split(":")[0]
	password = decryptedText.split(":")[1]
	
	return email, password


def getCourses(email, password):
	#--------------------------------
	# getLessons(email, password, fullCourseName)
	#
	
	waiting_time = 0
	arrLessonURL = []
	arrLessonTitle = []
	print "Getting courses list..."
	firstBrowser = 'phantomjs'
	secondBrowser = 'chrome'

	try:
		browser = Browser(firstBrowser)
		
	except:
		
		print "\nYou have not properly installed or configured PhantomJS!\nYou will see an automated browser popping up and crawling,\nwhich you will not see if you have properly installed or configured PhantomJS.\nDo not close that automated browser...\n"
		
		try:
			input("Press any key to continue...\n")
		except:
			pass

		try:
			browser = Browser(secondBrowser)
			print "Using Chrome Web Driver...\n"
			
		except:
			browser = Browser()
			print "Using Firefox Web Driver...\n"
		
	browser.driver.maximize_window()

	browser.visit('https://www.coursera.org/?authMode=login')

	browser.fill('email', email)
	browser.fill('password', password)
	
	button = browser.find_by_text('Log In')[-1]
	button.click()
	print "Welcome to Coursera!\n"
	time.sleep(15)
	
	while ('My Courses' not in browser.html):
		waiting_time = waiting_time +1
		sys.stdout.write('loading courses page...' + str(waiting_time) + " seconds\r")
		time.sleep(1)

	selector = 'div.headline-1-text.c-dashboard-course-course-name'

	courses = browser.find_by_css(selector)
	
	print "There are " + str(len(courses)) + " courses available\n"
	
	for i in range(0, len(courses)):
	
		print "["+str(i+1)+"] " + courses[i].text.encode('utf-8')
	
	print "\n"
	while True:
		sys.stdout.write("[  ] Please pick course number!\r")
		pick = raw_input("[")[:2]
		sys.stdout.write("[  ] second message!\r")
		try:
			pick = int(pick)
			break
		except:
			continue
		
	fullCourseName = courses[pick-1].text.encode('utf-8')
			
	print "\nYou have chosen: ["+str(pick)+"] " + fullCourseName + "\n"
	
	return fullCourseName
	
	try:
		print "\nClosing connection..."
		time.sleep(15)
		browser.driver.close()
	except:
		
		print footerText

			
def getLessons(email, password, fullCourseName):
	#--------------------------------
	# getLessons(email, password, fullCourseName)
	#
	
	firstBrowser = 'phantomjs'
	secondBrowser = 'chrome'

	try:
		browser = Browser(firstBrowser)
		
	except:
		
		print "\nYou have not properly installed or configured PhantomJS!\nYou will see an automated browser popping up and crawling,\nwhich you will not see if you have properly installed or configured PhantomJS.\nDo not close that automated browser...\n"
		
		try:
			browser = Browser(secondBrowser)
			print "Using Chrome Web Driver...\n"
			
		except:
			browser = Browser()
			print "Using Firefox Web Driver...\n"

	arrLessonURL = []
	arrLessonTitle = []
	
	browser.driver.maximize_window()

	browser.visit('https://www.coursera.org/?authMode=login')

	browser.fill('email', email)
	browser.fill('password', password)
	print "Logging in"
	button = browser.find_by_text('Log In')[-1]
	button.click()
	print "Welcome to Coursera"

	while(fullCourseName not in browser.html):
		
		sys.stdout.write('waiting for "' + fullCourseName[:48] + '" to appear...\r')
		#sys.stdout.flush()
		
	courses = browser.find_by_css('div.cozy.card-rich-interaction.c-dashboard-membership')
	sys.stdout.write('\n'+str(len(courses)) + ' lectures available\r\n\n')
	
	i = 0
	
	try:
	
		while(i < len(courses)):
		
			try:
			
				while(fullCourseName not in courses[i].text.encode('utf-8')):
				
					pass
					i += 1
					
				courses = browser.find_by_css('div.cozy.card-rich-interaction.c-dashboard-membership')[i].find_by_tag('a')[-1].click()
				
			except: # on StaleElementReferenceException
			
				browser.reload()
				
				while(fullCourseName not in browser.html):
			
					sys.stdout.write('waiting for "' + fullCourseName + '" to appear...\r')
					#sys.stdout.flush()
					
				courses = browser.find_by_css('div.cozy.card-rich-interaction.c-dashboard-membership')[i].find_by_tag('a')[-1].click()
				
	except:
	
		pass
		
	welcomepage = browser.url
	
	while(fullCourseName not in browser.html):
			
		sys.stdout.write('waiting for "' + fullCourseName + '" to appear...\r')
		sys.stdout.flush()
		
	weeks = browser.find_by_css('div.rc-WeekRow')
		
	sys.stdout.write('\n'+str(len(weeks)) + " weeks lecture\r\n")

	#sys.stdout.flush()
	
	for k in range(0, len(weeks)):
	
		url = welcomepage.replace('welcome','week/'+str(k+1))
		
		print "----------------- WEEK " + str(k+1) + "-----------------\n"
	
		browser.visit(url)
		
		time.sleep(5)
		
		selector = '#rendered-content > div > div.rc-OndemandApp > div.rc-HomeLayout > div.rc-HomeLayoutBody.horizontal-box > div.od-contents > main > div.rc-PeriodPage > div.horizontal-box.wrap > div > section > div.rc-LessonList.card-rich-interaction.od-section > div > div'
		
		items = browser.find_by_css(selector)
		
		sys.stdout.write('\n'+str(len(items)) + ' lessons available\r\n\n')
		

		for i in range (0, len(items)):
		
			try:
			
				print k+1, "-", i+1, items[i].find_by_css('h4').text.upper(), "\n"
			
				h5_items = items[i].find_by_css('h5')
				a_items = items[i].find_by_css('a')
				
				for j in range(0, len(h5_items)):
				
					url = a_items[j]['href']
					lessonTitle = h5_items[j].text
					
					print k+1, "-", i+1, "-", j+1, "-", lessonTitle, "\n", url
					
					arrLessonTitle.append(str(k+1).zfill(2) + "-" + str(i+1).zfill(2) + "-" + str(j+1).zfill(2) + "-" +lessonTitle)
					arrLessonURL.append(url)
									
				i += 1
				
				print "\n"
				
	
			except:
			
				browser.reload()
				
				time.sleep(5)
				
				print k+1, "-", i+1, items[i].find_by_css('h4').text.upper(), "\n"
			
				h5_items = items[i].find_by_css('h5')
				a_items = items[i].find_by_css('a')
				
				for j in range(0, len(h5_items)):
				
					url = a_items[j]['href']
					lessonTitle = h5_items[j].text
					
					print k+1, "-", i+1, "-", j+1, "-", lessonTitle, "\n", url
					
					arrLessonTitle.append(str(k+1).zfill(2) + "-" + str(i+1).zfill(2) + "-" + str(j+1).zfill(2) + "-" +lessonTitle)
					arrLessonURL.append(url)
					
				print "\n"
		
		time.sleep(5)
		
	print len(arrLessonTitle)," lessons", len(arrLessonURL), " urls"
		
	browser.driver.close()
	
	return arrLessonTitle, arrLessonURL



def checkCSV(fullCourseName):

	strNamaFile = cleanTitle(fullCourseName) + "-lessons.csv"

	if not os.path.isfile(strNamaFile):
	
		createCSV(fullCourseName)
		
	return strNamaFile


def createCSV(fullCourseName):

	arrLessonTitle, arrLessonURL = getLessons(email, password, fullCourseName)
	
	strNamaFile = cleanTitle(fullCourseName) + "-lessons.csv"
	
	f = open(strNamaFile, "w")
	
	f.close()
	
	f = open(strNamaFile, "a")
	
	for i in range (0, len(arrLessonTitle)):
	
		line = '"'+ str(i+1) + '","' + arrLessonURL[i]+'","' + arrLessonTitle[i] +'"\n'
		
		f.write(line)
		
	f.close()
	

	
	
	
def cleanTitle(strText):

	strText = strText.replace(":","")
	
	strText = strText.replace("/","")
	
	strText = strText.replace("?","")
	
	strText = strText.replace("  "," ")
	
	return strText
	
	
	
def fetchVideo(arrLessonTitle, arrLessonURL):

	firstBrowser = 'phantomjs'
	secondBrowser = 'chrome'

	try:
		browser = Browser(firstBrowser)
		
	except:
	
		print "\nYou have not properly installed or configured PhantomJS!\nYou will see an automated browser popping up and crawling,\nwhich you will not see if you have properly installed or configured PhantomJS.\nDo not close that automated browser...\n"
		
		try:
			browser = Browser(secondBrowser)
			print "Using Chrome Web Driver...\n"
			
		except:
			browser = Browser()
			print "Using Firefox Web Driver...\n"
	
	# if firstBrowser == 'chrome':
	
		# if disableImage == True:
		
			# browser.driver.close()
			# options = webdriver.ChromeOptions()
			# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
			# options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images":2})
			# browser.driver = webdriver.Chrome(chrome_options=options)
		
	browser.driver.maximize_window()

	browser.visit('https://www.coursera.org/?authMode=login')
	time.sleep(5)

	browser.fill('email', email)
	time.sleep(.5)
	browser.fill('password', password)
	print "Logging (back) in...\n"

	button = browser.find_by_text('Log In')[-1]
	button.click()
	
	print "Login success...\n\nWelcome to Coursera\n"

	for i in range(0, len(arrLessonURL)):
		
		browser.visit(arrLessonURL[i])
		
		strLessonTitle = arrLessonTitle[i][9:].replace("Reading: ","")
		
		if not precheck(strLessonTitle, fullCourseName):
				
			waiting_time = 0
			while(strLessonTitle not in browser.html):
			
				waiting_time = waiting_time + 1
				sys.stdout.write('waiting for "' + strLessonTitle[:48] + '" to appear...' + str(waiting_time) + ' second(s)\r')
				sys.stdout.flush()
				time.sleep(1)
				if waiting_time == 60:
					print('Time out. Skipped.')
					break
					
			try:
			
				selector = '#rendered-content > div > div.rc-OndemandApp > div.rc-ItemLayout > div:nth-child(3) > div > div > div > div.horizontal-box.week-drawer-container > div.content-container.flex-1 > div.extras.horizontal-box.align-items-top.wrap > div.rc-LectureResources.styleguide > ul > li'
				
				courses = browser.find_by_css(selector)
				
				for course in courses:
					
					strLessonURL = course.find_by_css('a')['href']
					print strLessonURL, "\n"
					fileName = cleanTitle(arrLessonTitle[i])
					print fileName, "\n"
					try:			

						while(getFile(strLessonURL, fileName, fullCourseName)):
												
							break
							
					except:
						print "download failed...\n"
				
			except:
			
				print "No video found.\n"
				pass
				
		else:
		
			pass

	browser.driver.close()



def precheck(strLessonTitle, fullCourseName):

	words = ['Quiz:', 'Reading:']
		
	checkResult = False
	
	fullCourseName = cleanTitle(fullCourseName)
	
	if any([word in strLessonTitle for word in words]):
	
		checkResult = True
		
	else:
	
		exts = ['.mp4','.vtt','.txt']
		
		checkResult = False
		
		print 'Checking existing downloads for: "' + strLessonTitle + '"'
		
		if not os.path.exists(scriptRoot + fullCourseName):
		
			os.mkdir(scriptRoot + fullCourseName)	

		files = os.listdir(scriptRoot + fullCourseName + os.sep)
				
		for file in files:
			
			if any([cleanTitle(strLessonTitle) in file for file in files]):
			
				checkResult = True or checkResult
				
				for ext in exts:
				
					if ext in file:
					
						checkResult = True or checkResult
					
						if (os.path.getsize(scriptRoot + fullCourseName + os.sep + file) == 0):
						
							#print "file found with size 0"
				
							checkResult = True and checkResult
					else:
					
						checkResult = False and checkResult
					
			#print file, checkResult
				
	return checkResult

			
	
def readCSV(strNamaFile):

	f = open(strNamaFile)
	
	arrLessonURL = []
	arrLessonTitle = []
	
	for line in f.readlines():
	
		strLessonTitle = re.findall('"[0-9]+-.*?"', line)[0].replace('"','')
		strLessonURL = re.findall('"http.*?"', line)[0].replace('"','')
		
		arrLessonTitle.append(strLessonTitle)
		arrLessonURL.append(strLessonURL)
		#print strLessonTitle,"\n", strLessonURL
		
	# "[0-9]+" --> regex to grab the number cell
	# "[0-9]+-.*?" --> regex to grab the title cell
	# "http.*?" ---> regex to grab the url cell
	f.close()
	return arrLessonURL, arrLessonTitle
	


def getFile(strLessonURL, strLessonTitle, fullCourseName):

	fileName = strLessonTitle
	
	fullCourseName = cleanTitle(fullCourseName)
	
	downloadedSize = 0
	
	if "index.mp4" in strLessonURL:
	
		fileName = strLessonTitle + ".mp4"
		
	if "Extension=vtt" in strLessonURL:
	
		fileName = strLessonTitle + ".vtt"
		
	if "Extension=txt" in strLessonURL:
	
		fileName = strLessonTitle + ".txt"
		
	print "getting file " + fileName
	
	if not os.path.exists(scriptRoot + fullCourseName):

		print "creating directories:", fullCourseName
		
		os.mkdir(scriptRoot + fullCourseName)	
	
	if not os.path.isfile(scriptRoot + fullCourseName + os.sep + fileName):
	
		os.chdir(scriptRoot + fullCourseName)
		
		f = open(fileName, 'wb')

		u = urllib2.urlopen(strLessonURL)

		meta = u.info()
			
		if "Content-Length" in meta:

			fileSize = int(meta.getheaders("Content-Length")[0])

			print "Downloading: %s Bytes: %s" % (fileName, fileSize)
				
			blockSize = 8192

			while True:

				buffer = u.read(blockSize)
					
				if not buffer:
					
					break

				downloadedSize += len(buffer)
					
				f.write(buffer)
					
				status = r"%10d  [%3.2f%%]" % (downloadedSize, downloadedSize * 100. / fileSize)
					
				status = status + chr(8)*(len(status)+1)
					
				print status,
					
		else:
				
			print "Downloading: unknown bytes..."
											
			f.write(u.read())

		f.close()
				
		print(fileName + " downloaded.\n")
			
		time.sleep(.3)
		
	else:
	
		print fileName +" already exists.\n"
		
	return True
	
	
	
def main():
	
	global email, password, fullCourseName
	
	fullCourseName = 'Machine Learning Foundations: A Case Study Approach'

	
	clearScreen()
	
	print headerText

	try:

		email, password = getUserPass("coursera.pass")
			
	except:

		createPass()
		print "User and password has been saved to coursera.pass file.\nPlease delete the file if you want to change your credentials.\n"
		email, password = getUserPass("coursera.pass")

			
	fullCourseName = getCourses(email, password)

	strNamaFile = checkCSV(fullCourseName)
	
	arrLessonURL, arrLessonTitle = readCSV(strNamaFile)
		
	fetchVideo(arrLessonTitle, arrLessonURL)
	
	print footerText
	
	
main()
#email, password = getUserPass("coursera.pass")
#getCourses(email, password)	