#-*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# coursera.py
# (c) Jansen A. Simanullang
# Automated Coursera Downloader
# START: 28.03.2016 18:17
# LAST: 03.04.2016 17:12
#---------------------------------------
# usage:
# python coursera.py
#
# changes:
# 01.04.2016: Courses list downloaded
# 03.04.2016: adjust string for multiple 16
#---------------------------------------
from splinter import Browser
from selenium import webdriver
import os, sys, re, time, urllib2, math, getpass
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
	
	#print("len: ", len(strInput), "multiples: ", multiples, "remainder: ", remainder)
	
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
	
	password = getpass.getpass('Enter your Coursera password: ')
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
	
	try:
		print "\nClosing connection..."
		time.sleep(15)
		browser.driver.close()
	except:
		
		print footerText

	return fullCourseName	
			
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

	arrWeeks = []		
	arrSectionTitle = []
	arrLessonTitle = []
	arrLectureTitle = []
	arrLectureURL = []

	
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
	#sys.stdout.write('\n'+str(len(courses)) + ' lectures available\r\n\n')
	
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
		
	sys.stdout.write('\n'+str(len(weeks)) + " week(s) lecture\r\n")

	#sys.stdout.flush()
	
	for k in range(0, len(weeks)):
	
		url = welcomepage.replace('welcome','week/'+str(k+1))
		
		print "----------------- WEEK " + str(k+1) + "-----------------\n"
	
		browser.visit(url)
		
		time.sleep(5)
		
		#selector = '#rendered-content > div > div.rc-OndemandApp > div.rc-HomeLayout > div.rc-HomeLayoutBody.horizontal-box > div.od-contents > main > div.rc-PeriodPage > div.horizontal-box.wrap > div > section > div.rc-LessonList.card-rich-interaction.od-section > div > div'
		
		selector = '#rendered-content > div > div.rc-OndemandApp > div > div.rc-HomeLayout > div.rc-HomeLayoutBody > main.od-contents.vertical-box > div.c-body > div.rc-PeriodPage > div.horizontal-box.wrap > div.flex-1 > section.rc-ModuleSection.od-section' # '> div.rc-ModuleLessons > div.od-section > div.rc-LessonCollectionBody > div.card-rich-interaction.od-lesson-collection-container > div.od-lesson-collection-element > div.rc-NamedItemList > span.rc-ItemHonorsWrapper.nostyle'
		
		sections = browser.find_by_css(selector)
		
		sys.stdout.write('\n'+str(len(sections)) + ' section(s) available\r\n\n')
		
		for i in range (0, len(sections)):
		
			sectionTitle = sections[i].find_by_css('div > h5.tab-headline > span').text
			print "section", i+1, ":", sectionTitle , "\n" 
			lessons = sections[i].find_by_css('div.rc-ModuleLessons > div.od-section > div.rc-LessonCollectionBody > div.card-rich-interaction.od-lesson-collection-container > div.od-lesson-collection-element > div.rc-NamedItemList')
			lectureLessons = []
			for lesson in lessons:
				items = lesson.find_by_css('span.rc-ItemHonorsWrapper.nostyle')
				for item in items:
					if 'lecture' in item.find_by_css('a')['href']:
						lectureLessons.append(lesson)
						break
						
			print len(lectureLessons) , "lesson(s) available\n"
				
			for j in range(0, len(lectureLessons)):
				lessonTitle = lectureLessons[j].find_by_css('div.horizontal-box.named-item-list-title > h4').text
				print "lesson" , j+1, ":", lessonTitle
				lectures = []
				items = lectureLessons[j].find_by_css('span.rc-ItemHonorsWrapper.nostyle')
				for item in items:
					if 'lecture' in item.find_by_css('a')['href']:
						lectures.append(item)
							
				print len(lectures), "lecture(s) available\n"
				for w in range(0,len(lectures)):
					h5_item = lectures[w].find_by_css('h5')
					a_item = lectures[w].find_by_css('a')
				
					url = a_item['href']
					lectureTitle = h5_item.text
					
					print w+1, "-", lectureTitle, "\n", url
						
					arrWeeks.append("week" + str(k+1).zfill(2))
					arrSectionTitle.append(str(i+1).zfill(2) + "-" + sectionTitle)
					arrLessonTitle.append(str(j+1).zfill(2) + "-" + lessonTitle)
					arrLectureTitle.append(str(w+1).zfill(2) + "-" + lectureTitle)
					arrLectureURL.append(url)
									
				
				
			print "\n"
		
		time.sleep(5)
		
	print len(arrLessonTitle),"lectures", len(arrLectureURL), "urls"
		
	browser.driver.close()
	
	return arrWeeks, arrSectionTitle, arrLessonTitle, arrLectureTitle, arrLectureURL



def checkCSV(fullCourseName):

	strNamaFile = cleanTitle(fullCourseName) + "-lectures.csv"

	if not os.path.isfile(strNamaFile):
	
		createCSV(fullCourseName)
		
	return strNamaFile


def createCSV(fullCourseName):

	arrWeeks, arrSectionTitle, arrLessonTitle, arrLectureTitle, arrLectureURL = getLessons(email, password, fullCourseName)
	
	strNamaFile = cleanTitle(fullCourseName) + "-lectures.csv"
	
	f = open(strNamaFile, "w")
	
	f.close()
	
	f = open(strNamaFile, "a")
	
	for i in range (0, len(arrLectureTitle)):
	
		line = '"'+ arrWeeks[i] + '","' + arrSectionTitle[i] + '","' +  arrLessonTitle[i] + '","' + arrLectureTitle[i]+'","' + arrLectureURL[i] +'"\n'
		
		f.write(line)
		
	f.close()
	

def cleanTitle(strText):

	strText = strText.replace(":","")
	
	strText = strText.replace("/","")
	
	strText = strText.replace("?","")
	
	strText = strText.replace("  "," ")
	
	return strText
	
	
	
def fetchVideo(arrWeeks, arrSectionTitle, arrLessonTitle, arrLectureTitle, arrLectureURL):

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

	for i in range(0, len(arrLectureURL)):
		
		browser.visit(arrLectureURL[i])
		
		strLectureTitle = arrLectureTitle[i][3:]
		
		if not precheck(arrWeeks[i], arrSectionTitle[i], arrLessonTitle[i], arrLectureTitle[i], strLectureTitle, fullCourseName):
				
			waiting_time = 0
			while(strLectureTitle not in browser.html):
			
				waiting_time = waiting_time + 1
				sys.stdout.write('waiting for "' + strLectureTitle[:48] + '" to appear...' + str(waiting_time) + ' second(s)\r')
				sys.stdout.flush()
				time.sleep(1)
				if waiting_time == 60:
					print('Time out. Skipped.')
					break
					
			try:
			
				#selector = '#rendered-content > div > div.rc-OndemandApp > div.rc-ItemLayout > div:nth-child(3) > div > div > div > div.horizontal-box.week-drawer-container > div.content-container.flex-1 > div.extras.horizontal-box.align-items-top.wrap > div.rc-LectureResources.styleguide > ul > li'
				
				selector = '#rendered-content > div > div.rc-OndemandApp > div > div.rc-ItemLayout > div > div.rc-VideoItem > div.horizontal-box > div.rc-ItemNavigation > div.horizontal-box.week-drawer-container > div.flex-1 > div.content-container > div.extras.horizontal-box.align-items-top.wrap > div.rc-LectureResources.styleguide.flex-1 > ul.resources-list.card-rich-interaction > li'
				
				courses = browser.find_by_css(selector)
				
				for course in courses:
					strLectureDownloadURL = course.find_by_css('a')['href']
					print strLectureDownloadURL, "\n"
					fileName = cleanTitle(arrLectureTitle[i])
					print fileName, "\n"
					try:			

						while(getFile(arrWeeks[i], arrSectionTitle[i], arrLessonTitle[i], strLectureDownloadURL, fileName, fullCourseName)):
												
							break
							
					except:
						print "download failed...\n"
				
			except:
			
				print "No video found.\n"
				pass
				
		else:
		
			pass

	browser.driver.close()



def precheck(arrWeeks, arrSectionTitle, arrLessonTitle, arrLectureTitle, strLectureTitle, fullCourseName):

	checkResult = False
	
	fullCourseName = cleanTitle(fullCourseName)
	
	arrSectionTitle = cleanTitle(arrSectionTitle)
	
	arrLessonTitle = cleanTitle(arrLessonTitle)
	
	arrLectureTitle = cleanTitle(arrLectureTitle)
	
	exts = ['.mp4','.vtt','.txt']
		
	print 'Checking existing downloads for: "' + strLectureTitle + '"'
		
	if not os.path.exists(scriptRoot + fullCourseName):
		
		os.mkdir(scriptRoot + fullCourseName)	

	if not os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks):
		
		os.mkdir(scriptRoot + fullCourseName + os.sep + arrWeeks)
		
	if not os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle):
		
		os.mkdir(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle)
			
	if not os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle):
		
		os.mkdir(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle)
			
	if not os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle):
		
		os.mkdir(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle)
	
	files = os.listdir(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle + os.sep)
				
	for file in files:
			
		if any([cleanTitle(strLectureTitle) in file for file in files]):
		
			checkResult = True or checkResult
				
			for ext in exts:
				
				if ext in file:
					
					checkResult = True or checkResult
					
					if os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle + os.sep + file):
						
						if (os.path.getsize(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle + os.sep + file) == 0):
					
							#print "file found with size 0"
				
							checkResult = True and checkResult
				else:
					
					checkResult = False and checkResult
					
		#print file, checkResult
				
	return checkResult
	
def readCSV(strNamaFile):

	f = open(strNamaFile)
	
	arrWeeks = []
	arrSectionTitle = []
	arrLessonTitle = []
	arrLectureTitle = []
	arrLectureURL = []
	
	for line in f.readlines():
	
		week = re.findall('"week[0-9]+?"', line)[0].replace('"','')
		sectionTitle = re.findall('"[0-9]+-.*?"', line)[0].replace('"','')
		lessonTitle = re.findall('"[0-9]+-.*?"', line)[1].replace('"','')
		lectureTitle = re.findall('"[0-9]+-.*?"', line)[2].replace('"','')
		lectureURL = re.findall('"http.*?"', line)[0].replace('"','')
		
		arrWeeks.append(week)
		arrSectionTitle.append(sectionTitle)
		arrLessonTitle.append(lessonTitle)
		arrLectureTitle.append(lectureTitle)
		arrLectureURL.append(lectureURL)
		#print strLessonTitle,"\n", strLessonURL
		
	# "[0-9]+" --> regex to grab the number cell
	# "[0-9]+-.*?" --> regex to grab the title cell
	# "http.*?" ---> regex to grab the url cell
	f.close()
	return arrWeeks, arrSectionTitle, arrLessonTitle, arrLectureTitle, arrLectureURL
	


def getFile(arrWeeks, arrSectionTitle, arrLessonTitle, strLectureDownloadURL, arrLectureTitle, fullCourseName):

	fileName = arrLectureTitle
	
	fullCourseName = cleanTitle(fullCourseName)
	
	arrSectionTitle = cleanTitle(arrSectionTitle)

	arrLessonTitle = cleanTitle(arrLessonTitle)
	
	downloadedSize = 0
	
	if "index.mp4" in strLectureDownloadURL:
	
		fileName = arrLectureTitle + ".mp4"
		
	if "Extension=vtt" in strLectureDownloadURL:
	
		fileName = arrLectureTitle + ".vtt"
		
	if "Extension=txt" in strLectureDownloadURL:
	
		fileName = arrLectureTitle + ".txt"
		
	print "getting file " + fileName
	
	if not os.path.exists(scriptRoot + fullCourseName):
		
		os.mkdir(scriptRoot + fullCourseName)
	
	if not os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks):
		
		os.mkdir(scriptRoot + fullCourseName + os.sep + arrWeeks)
		
	if not os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle):
		
		os.mkdir(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle)
			
	if not os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle):
		
		os.mkdir(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle)
			
	if not os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle):
		
		os.mkdir(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle)
	
	if not os.path.exists(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle + os.sep + fileName):
		
		if not os.path.isfile(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle + os.sep + fileName):
		
			os.chdir(scriptRoot + fullCourseName + os.sep + arrWeeks + os.sep + arrSectionTitle + os.sep + arrLessonTitle + os.sep + arrLectureTitle)
			
			f = open(fileName, 'wb')
	
			u = urllib2.urlopen(strLectureDownloadURL)
	
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
	
	arrWeeks, arrSectionTitle, arrLessonTitle, arrLectureTitle, arrLectureURL = readCSV(strNamaFile)
		
	fetchVideo(arrWeeks, arrSectionTitle, arrLessonTitle, arrLectureTitle, arrLectureURL)
	
	print footerText
	
	
main()
