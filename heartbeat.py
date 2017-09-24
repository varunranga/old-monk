import tflearn
import pandas as pd
import numpy as np

df = pd.read_csv('Heartbeat.csv')
inputY = df['class']
inputY = np.array(inputY)

df = df.drop('class', axis = 1)
inputX = np.array(df)

inputYOneHot = []
for c in inputY:
	if(c == 1):
		inputYOneHot.append([1, 0])
	else:
		inputYOneHot.append([0, 1])

inputY = np.array(inputYOneHot)

net = tflearn.input_data(shape=[None, 13])
net = tflearn.fully_connected(net, 17)
net = tflearn.fully_connected(net, 19)
net = tflearn.fully_connected(net, 15)
net = tflearn.fully_connected(net, 2, activation='softmax')
net = tflearn.regression(net, optimizer = 'SGD', learning_rate = 0.01)

model = tflearn.DNN(net)

model.fit(inputX, inputY, n_epoch = 100, validation_set = 0.1, batch_size = 1, show_metric=True, run_id='Old Monk')

model.save('heartbeat.model')