import pandas as pd 
import matplotlib
import math
import pickle
import threading
import matplotlib.pyplot as plt
import statistics as stat 


file=open("sleepData.pickle","rb")
value=[]
value=pickle.load(file)
file.close()


lenVal=len(value)
heartBeat=[]
modX=[]

for j in range(len(value)):
	if ('aworld' in str(value[j])):
		break

for i in range(j, len(value), 2):
	try:
		data=str(value[i])[2:-1] + str(value[i+1])[2:-1]
	except:
		break

	#print(data)
	val=data.split('\\r')
	#print(val)
	acceleration=val[0].split('\\t')
	accelerationX=float(acceleration[1])
	accelerationY=float(acceleration[2])
	accelerationZ=float(acceleration[3])
	#print(accelerationX)
	#print(accelerationY)
	#print(accelerationZ)
	len1=len(val[1])
	#print(len1)

	bpm=0

	for i in range(7,len1):
		bpm=bpm*10+float(val[1][i])

	heartBeat.append(bpm)
	#print(i)
	#print("BPM :",bpm)
	#print("X :",accelerationX)
	#print("Y :",accelerationY)
	#print("Z :",accelerationZ)

	accelerationZ-=500

	modValue=math.sqrt((accelerationX*accelerationX  + accelerationY*accelerationY + accelerationZ*accelerationZ))
	modX.append(modValue)
	#print("Mod Value :",modValue)
	#print("\n")

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


def plotHeartrate():
	plt.plot(x, heartBeat, '-o')
	#plt.axis([0, 6, 0, 20])
	plt.show()
	#import statistics as stat
	avgHeartBeat=stat.mean(heartBeat)
	print("Average Heart Beat : ",avgHeartBeat)

plotSleep()
plotHeartrate()