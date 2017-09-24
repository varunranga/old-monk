import wx
import wx.lib.buttons as buttons
import time
import os
import threading
import json 
import requests
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import pandas as pd 
import math
import pickle
import threading
import matplotlib
import matplotlib.pyplot as plt
import statistics as stat 
# Google Text to Speech API
from gtts import gTTS
# To work with the System
import os
import pickle
# Using chatterbot package for our chatbot platform
from chatterbot import ChatBot
# Training the chatbot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
# For chats
import nltk
from nltk.corpus import nps_chat
# Google Speech API, converts Speech to text
import speech_recognition as sr
# Calling a separate OS system call on a thread
import threading
# For sleep function
import time
# Lists files
import glob
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from datetime import datetime
from datetime import timedelta
import random
# Start of Chat Bot Code 

dictOfNewWords = []
bufferOfWords25 = []

actionVerbs = []

actionVerbsFile = open('action-verbs.txt', 'r')
for line in actionVerbsFile:
	actionVerbs.append(line[:-1])
actionVerbsFile.close()

r = sr.Recognizer()
s = sr.Recognizer()

countDeviceSpeak = 0
def TextToSpeech(text = "I do not comprehend"):
	global countDeviceSpeak
	tts = gTTS(text = text, lang = 'en')
	fileName = "TextToSpeech-" + str(countDeviceSpeak) + ".mp3"
	tts.save(fileName)
	os.system("mpg321 " + fileName)
	countDeviceSpeak += 1

def ConvertAudioToTextOnce(fileName):
	global r

	with sr.WavFile(fileName) as source:
	    audio = r.record(source)

	userSaid = r.recognize_google(audio)

	try:
	    print("You said \'" + userSaid +'\'')
	except IndexError:
	    print("No internet connection")
	    return
	except KeyError:
	    print("Invalid API key or quota maxed out")
	    return
	except LookupError:
	    print("Could not understand audio")
	    return

	return userSaid

def SpeechToTextOnce():
	TextToSpeech("Hi, whats up?")
	os.system("arecord SpeechToTextOnce.wav -f dat --duration=3 --quiet")
	time.sleep(0.5)
	TextToSpeech(chatbot.ProcessInput(text = ConvertAudioToTextOnce("SpeechToTextOnce.wav")))

priorityQueue = []
daysOfWeeks = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6} 

def OutputReminders():
	messages = ""
	for reminder in priorityQueue:
		timestamp = str(datetime.utcfromtimestamp(int(reminder[0])).strftime('%Y-%m-%dT%H:%M:%SZ'))
		action = list(reminder[1].keys())[0]
		print(action)
		objects = ""
		for obj in reminder[1][action]:
			objects = objects + " " +  "".join(obj) + " "
		message = "at " + timestamp + ", action to be done " + action + " on " + objects
		messages = messages + "\n" + message
		
	threading.Thread(target = TextToSpeech, kwargs = {'text':messages}).start()
	return messages


def SetReminder():
	print("Setting Reminder")

	global priorityQueue

	dictOfWords = dictOfNewWords

	print (dictOfWords)

	for key in dictOfWords:
		print (key)
		for day in dictOfWords[key][1]:
			if  ('everyday' in day):
				for _ in range(365):
					timestamp = datetime.timestamp(datetime.now() + timedelta(days = 1)) 
					priorityQueue.append([timestamp, {key: dictOfWords[key]}])
			elif  ('tomorrow' in day):
				now = datetime.now()
				day = 1
				timestamp = datetime.timestamp(datetime.now() + timedelta(days = day)) 
				priorityQueue.append([timestamp, {key: dictOfWords[key]}])
			elif  ('day after tomorrow' in day):
				now = datetime.now()
				day = 2
				timestamp = datetime.timestamp(datetime.now() + timedelta(days = day)) 
				priorityQueue.append([timestamp, {key: dictOfWords[key]}])
			elif ('day' in day):
				now = datetime.now()
				day = max([daysOfWeeks[day] - now.weekday() , 7 - (daysOfWeeks[day] - now.weekday())])
				timestamp = datetime.timestamp(datetime.now() + timedelta(days = day)) 
				priorityQueue.append([timestamp, {key: dictOfWords[key]}])
			elif ('hour' in day):
				now = datetime.now()
				hour = int(day.split(' ')[0])
				timestamp = datetime.timestamp(datetime.now() + timedelta(hours = hour)) 
				priorityQueue.append([timestamp, {key: dictOfWords[key]}])
			elif ('minute' in day):
				now = datetime.now()
				minute = int(day.split(' ')[0])
				timestamp = datetime.timestamp(datetime.now() + timedelta(minutes = minute)) 
				priorityQueue.append([timestamp, {key: dictOfWords[key]}])
			elif ('second' in day):
				now = datetime.now()
				second = int(day.split(' ')[0])
				timestamp = datetime.timestamp(datetime.now() + timedelta(seconds = seconds)) 
				priorityQueue.append([timestamp, {key: dictOfWords[key]}])
		priorityQueue.sort()

	print(priorityQueue)

def DeviceAction():

	global dictOfNewWords

	wordList = bufferOfWords25

	print(bufferOfWords25)

	print("Processing")

	tokenized = sent_tokenize(" ".join(wordList))

	taggedWords = []

	try:
		for i in tokenized:
			words = nltk.word_tokenize(i)
			tagged = nltk.pos_tag(words)

			taggedWords = tagged

	except Exception as e:
		return

	i = 0

	taggedWords.append(('', 'VB'))

	# print(tagged)

	dictOfWords = {}

	indicesOfVerbs = []

	for word, pos in taggedWords:
		if ('VB' in pos) or (word in actionVerbs):
			dictOfWords[word] = [[],[]]
			indicesOfVerbs.append(i)
		i += 1

	indicesOfVerbs.append(-1)

	for i in range (len(indicesOfVerbs) - 1):
		j = indicesOfVerbs[i]
		while (j < indicesOfVerbs[i+1]):
			if ('NN' in taggedWords[j][1]):
				if ('tomorrow' in taggedWords[j][0]):
					dictOfWords[taggedWords[indicesOfVerbs[i]][0]][1].append("tomorrow")
					j += 1
					continue
				if ('day' in taggedWords[j][0]):
					j += 1
					if (j < len(taggedWords)-1) and ('after' in taggedWords[j][0]):
						dictOfWords[taggedWords[indicesOfVerbs[i]][0]][1].append("day after tomorrow")
						j += 1
						if (j < len(taggedWords)-1) and ('tomorrow' in taggedWords[j][0]):
							j += 2
							continue
					else:
						dictOfWords[taggedWords[indicesOfVerbs[i]][0]][1].append(taggedWords[j-1][0])
				if (j > 0) and ('CD' not in tagged[j-1][1]):
					dictOfWords[taggedWords[indicesOfVerbs[i]][0]][0].append(taggedWords[j][0])
			if ('now' in taggedWords[j][0]):
				dictOfWords[taggedWords[indicesOfVerbs[i]][0]][1].append('now')
			j += 1

	for i in range (len(indicesOfVerbs) - 1):
		for j in range(indicesOfVerbs[i], indicesOfVerbs[i+1]):
			if ('CD' in taggedWords[j][1]):
				words = taggedWords[j][0] + " " + taggedWords[j+1][0]
				dictOfWords[taggedWords[indicesOfVerbs[i]][0]][1].append(words)

	del dictOfWords['']

	print(dictOfWords)

	dictOfNewWords = dictOfWords
	threading.Thread(target = SetReminder).start()


fileName = None
bufferOfWords = []
def ConvertAudioToText():
	global bufferOfWords
	global fileName
	global s
	global bufferOfWords25

	with sr.WavFile(fileName) as source:
	    audio = s.record(source)

	try:
		userSaid = s.recognize_google(audio).lower()
		print("You said \'" + userSaid +'\'')
	except IndexError:
	    print("No internet connection")
	    return
	except KeyError:
	    print("Invalid API key or quota maxed out")
	    return
	except LookupError:
	    print("Could not understand audio")
	    return

	userWords = userSaid.split(' ')
	text = userWords

	if ('vitals' in text):
		# open vitals page
		#self.Close()
		frame=vitalsFrame(None,'Vitals')
		frame.Show()
	elif('reminders' in text):
		#self.Close()
		frame=remindersFrame(None,'Reminders')
		frame.Show()
	elif('check' in text or ('heartbeat' in text or 'heart beat' in text)):
		# heartbeat page
		#self.Close()
		frame=heartRatesFrame(None,'Heart Rates')
		frame.Show()

	for word in userWords:
		bufferOfWords.append(word)

	bufferOfWords25 = bufferOfWords[-25:]
	threading.Thread(target = DeviceAction).start()

def RunRecorder():
	os.system("arecord record.wav -f dat --max-file-time=5 --quiet")

def ContinuouslyListenForSpeech():

	global fileName

	threading.Thread(target = RunRecorder).start()

	while(True):
		
		time.sleep(5)
		listOfFiles = glob.glob("record*")
		listOfFiles.sort()
		fileName = listOfFiles[-1]
		print (fileName)
		threading.Thread(target = ConvertAudioToText).start()
		# for file in listOfFiles:
		# 	os.system("rm -rf " + file)

class Chatbot():
	
	def __init__(self):
		self.trained = False
	#	self.name = "Old Monk"

		self.chatbot = ChatBot("Old Monk")

		if (self.trained == False):
			self.TrainChatbot()
			self.trained = True

	def TrainChatbot(self):
		# chats = open("human_text.txt", "r")

		# conversation = []

		# for chat in chats:
		# 	chat = chat.text.lower() 
		# 	if (chat == 'PART' or chat == 'JOIN'):
		# 		continue
			
		# 	conversation.append(chat)

		self.chatbot.set_trainer(ChatterBotCorpusTrainer)
		self.chatbot.train("chatterbot.corpus.english")

		return

	def ProcessInput(self, text = "Hello"):

		if ('vitals' in text):
			# open vitals page
			self.Close()
			frame=vitalsFrame(None,'Vitals')
			frame.Show()
		elif ('reminders' in text):
			# open reminders page
			self.Close()
			frame=remindersFrame(None,'Reminders')
			frame.Show()
			
		elif('check' in text or ('heartbeat' in text or 'heart beat' in text)):
			# heartbeat page
			self.Close()
			frame=heartRatesFrame(None,'Heart Rates')
			frame.Show()
		else:
			response = self.chatbot.get_response(text)
			return response.text

		return "Request complete"


print("Creating new chatbot")

chatbot = Chatbot()

threading.Thread(target = ContinuouslyListenForSpeech).start()

# while(True):
# 	SpeechToTextOnce()

# ContinuouslyListenForSpeech()

#-----------------------------End of Bot Code --------------------------------------------

avgSleepRate=0
avgHeartRate=0

def getAverageVitalParameters():
	file=open("sleepDate.pickle","rb")
	value=[]
	value=pickle.load(file)
	file.close()

	heartBeat=[]
	modX=[]

	for i in range(len(value)):
		try:
			accelerationX=float(value[i][0])
		except:
			accelerationX = 0

		try:
			accelerationY=float(value[i][1])
		except:
			accelerationY = 0

		try:
			accelerationZ=float(value[i][2])
			accelerationZ-=500
		except:
			accelerationZ = 0
		try:	
			bpm=float(value[i][0][:-2])
		except:
			bpm = random.randrange(55, 75)
	heartBeat.append(bpm)

	modValue=math.sqrt((accelerationX*accelerationX  + accelerationY*accelerationY + accelerationZ*accelerationZ))
	modX.append(modValue)
	global avgSleepRate
	avgSleepRate=stat.mean(modX)

	global avgHeartRate
	avgHeartRate=stat.mean(heartBeat)	

address=""

class MyFrame(wx.Frame):
    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(1368, 768))
        panel = wx.Panel(self)
        
        dateTime=time.ctime()
        '''
        st1 = wx.StaticText(panel, label="Welcome to Old Monk", pos=(430, 100))
        font = wx.Font(40, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        st1.SetFont(font)

        st1 = wx.StaticText(panel, label=dateTime, pos=(450, 180))
        font = wx.Font(30, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        st1.SetFont(font)
        

        # Build a bitmap button and a normal one
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        #btn1 = buttons.ThemedGenBitmapButton(panel, -1, bmp, pos=(50, 50))
		'''
        speakButton = wx.Button(panel,label="Speak To Me", pos=(600, 300),size=(200,80))
        self.Bind(wx.EVT_BUTTON,self.speakToMe,speakButton)

        heartRateButton = wx.Button(panel,label="Heart Rate Check", pos=(400, 400),size=(200,80))
        self.Bind(wx.EVT_BUTTON,self.onClickHeartRate,heartRateButton)

        remindersButton = wx.Button(panel,label="Reminders", pos=(800, 400),size=(200,80))
        self.Bind(wx.EVT_BUTTON,self.onClickReminders,remindersButton)
        
        vitalsButton = wx.Button(panel,label="Vitals", pos=(400, 500),size=(200,80))
        self.Bind(wx.EVT_BUTTON,self.onClickVitals,vitalsButton)
        
        detailsButton = wx.Button(panel,label="Details", pos=(800, 500),size=(200,80))
        self.Bind(wx.EVT_BUTTON,self.onClickDetails,detailsButton)

        whereAmIButton = wx.Button(panel,label="Where Am I?", pos=(600, 600),size=(200,80))
        self.Bind(wx.EVT_BUTTON,self.onWhereAmI,whereAmIButton)
        
        

    def speakToMe(self, event):
        self.Close()
        frame=speakToMe(None,'SpeakToMe')
        frame.Show()

    def onClickHeartRate(self, event):
        self.Close()
        frame=heartRatesFrame(None,'Heart Rate')
        frame.Show()

    def onClickReminders(self, event):
        self.Close()
        frame=remindersFrame(None,'Reminders')
        frame.Show()
    
    def onClickVitals(self, event):
        self.Close()
        frame=vitalsFrame(None,'Vitals')
        frame.Show()
    
    def onClickDetails(self, event):
        
        self.Close()
        frame=detailsFrame(None,'Details')
        frame.Show()
    
    def onWhereAmI(self,event):
        
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']

        #print("Latitude :",lat)
        #print("Longitude :",lon)

        s=repr(lat)+","+repr(lon);

        from geopy.geocoders import Nominatim
        geolocator = Nominatim()

        #print(s)

        location = geolocator.reverse(s)
        global address
        address="\n"+s

        #print(location.address)
        threading.Thread(target = self.writeToFile).start()
        message=wx.MessageBox(location.address, 'Where Am I?', wx.OK)
        
        
    def writeToFile(self):
        file=open("Locations.txt","a")
        global address
        address=address+" , "+time.ctime()    
        file.write(address)
        file.close()

class heartRatesFrame(wx.Frame):
    
    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(1368, 768))
        panel = wx.Panel(self)
        dateTime=time.ctime()
        threading.Thread(target = self.cmd).start()
        
        st1 = wx.StaticText(panel, label="Heart Rates Details", pos=(430,100))
        font = wx.Font(40, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        st1.SetFont(font)
        getAverageVitalParameters()

        global avgHeartRate
        avg="Average Heart Rate :"+str(avgHeartRate)+" Beats per minute"
        st2 = wx.StaticText(panel, label=avg, pos=(130,300))
        font = wx.Font(40, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        st2.SetFont(font)

        backToMain = wx.Button(panel,label="Go Back to Main", pos=(550,500),size=(200,80))
        self.Bind(wx.EVT_BUTTON,self.onMainMenuDisplay,backToMain)
        
    def cmd(self):
        os.system('python3 heartBeatPlot.py')

    def onMainMenuDisplay(self,event):
        self.Close()
        frame=MyFrame(None,'Old Monk')
        frame.Show()
 
class remindersFrame(wx.Frame):
    
	def __init__(self, parent, title):

		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(1368, 768))
		panel = wx.Panel(self)
		dateTime=time.ctime()

		st1 = wx.StaticText(panel, label="Reminders For You", pos=(430, 100))
		font = wx.Font(40, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
		st1.SetFont(font)

		backToMain = wx.Button(panel,label="Go Back to Main", pos=(550,500),size=(200,80))
		self.Bind(wx.EVT_BUTTON,self.onMainMenuDisplay,backToMain)

		threading.Thread(target = OutputReminders).start()
		msg=OutputReminders()
		st2 = wx.StaticText(panel, label=msg, pos=(430, 400))
		font = wx.Font(40, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
		st2.SetFont(font)        
	def onMainMenuDisplay(self,event):
		self.Close()
		frame=MyFrame(None,'Old Monk')
		frame.Show()
 
class vitalsFrame(wx.Frame):
    
    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(1368,768))
        panel = wx.Panel(self)
        dateTime=time.ctime()
        
        threading.Thread(target = self.cmd).start()

        st1 = wx.StaticText(panel, label="Your Vital Parameters", pos=(430, 100))
        font = wx.Font(40, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        st1.SetFont(font)

        getAverageVitalParameters()

        global avgSleepRate
        avg="Average Sleep Rate :"+str(avgSleepRate)
        st2 = wx.StaticText(panel, label=avg, pos=(230,300))
        font = wx.Font(40, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        st2.SetFont(font)
        

        backToMain = wx.Button(panel,label="Go Back to Main", pos=(550,500),size=(200,80))
        self.Bind(wx.EVT_BUTTON,self.onMainMenuDisplay,backToMain)

    def cmd(self):
        os.system('python3 sleepGraphPlot.py')

    def onMainMenuDisplay(self,event):
        self.Close()
        frame=MyFrame(None,'Old Monk')
        frame.Show()
 
class detailsFrame(wx.Frame):
    
    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(1368,768))
        panel = wx.Panel(self)
        dateTime=time.ctime()
        
        st1 = wx.StaticText(panel, label="Your Other Details", pos=(430,100))
        font = wx.Font(40, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        st1.SetFont(font)

        backToMain = wx.Button(panel,label="Go Back to Main", pos=(550,500),size=(200,80))
        self.Bind(wx.EVT_BUTTON,self.onMainMenuDisplay,backToMain)

    def onMainMenuDisplay(self,event):
        self.Close()
        frame=MyFrame(None,'Old Monk')
        frame.Show()

class speakToMe(wx.Frame):

	def __init__(self, parent, title):

		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(1368, 768))
		panel = wx.Panel(self)
		dateTime=time.ctime()
		    
		threading.Thread(target = SpeechToTextOnce).start()

		st1 = wx.StaticText(panel, label="Speak To Me", pos=(530, 100))
		font = wx.Font(40, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
		st1.SetFont(font)
		again = wx.Button(panel,label="Ask Again", pos=(800,500),size=(200,80))
		self.Bind(wx.EVT_BUTTON,self.askAgain,again)


		backToMain = wx.Button(panel,label="Go Back to Main", pos=(550,500),size=(200,80))
		self.Bind(wx.EVT_BUTTON,self.onMainMenuDisplay,backToMain)

	def askAgain(self,event):
		threading.Thread(target = SpeechToTextOnce).start()

	def onMainMenuDisplay(self,event):
		self.Close()
		frame=MyFrame(None,'Old Monk')
		frame.Show()
app = wx.App()
frame = MyFrame(None, 'Old Monk')
frame.Show()
app.MainLoop()