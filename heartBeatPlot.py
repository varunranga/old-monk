import pandas as pd 
import matplotlib
import math
import pickle
import threading
import matplotlib.pyplot as plt
import statistics as stat 
import random


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

x=[]

l=len(modX)
for i in range(1,l+1):
	x.append(i)

def plotSleep():

	plt.plot(x, modX, '-o')
	#plt.axis([0, 6, 0, 20])
	plt.show()
	averageSleepAcceleration=stat.mean(modX)
	print("Average Sleep Acceleration:,",averageSleepAcceleration)

x=[]
l=len(heartBeat)
for i in range(1,l+1):
	x.append(i)
print(l)
def plotHeartrate():
	plt.plot(x, heartBeat, '-o')
	plt.axis([0, 300, 30, 120])
	plt.show()
	#import statistics as stat
	avgHeartBeat=stat.mean(heartBeat)
	print("Average Heart Beat : ",avgHeartBeat)

#plotSleep()
plotHeartrate()