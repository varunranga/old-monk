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
	os.system("mpg321 --quiet " + fileName)
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
	TextToSpeech("Tell me, what can I help you with?")
	os.system("arecord SpeechToTextOnce.wav --duration=5 --quiet")
	time.sleep(0.5)
	TextToSpeech(chatbot.ProcessInput(text = ConvertAudioToTextOnce("SpeechToTextOnce.wav")))



priorityQueue = []
daysOfWeeks = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6} 

def OutputReminders(n = 1):
	for reminder in priorityQueue[:n]:
		timestamp = str(datetime.datetime.utcfromtimestamp(int(reminder[0])).strftime('%Y-%m-%dT%H:%M:%SZ'))
		action = list(reminder.keys())[0]
		objects = ""
		for obj in reminder[action]:
			objects += obj + " "
		message = "at " + timestamp + ", action to be done " + action + " on " + objects
		TextToSpeech(text = message)


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

	for word in userWords:
		bufferOfWords.append(word)

	bufferOfWords25 = bufferOfWords[-25:]
	threading.Thread(target = DeviceAction).start()

def RunRecorder():
	os.system("arecord record.wav --max-file-time=5 --quiet")

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
		self.chatbot.train("chatterbot.corpus.english.conversations")

		return

	def ProcessInput(self, text = "Hello"):

		if ('vitals' in text):
			# open vitals page
		elif ('reminders' in text):
			# open reminders page
		elif('check' in text and ('heartbeat' in text or 'heart beat' in text)):
			# heartbeat page
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