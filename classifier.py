import tflearn
import tensorflow as tf
from tflearn.layers.conv import conv_1d, max_pool_1d, global_max_pool
import numpy as np
from tflearn.layers.merge_ops import merge

#fully connected neural net
def modelBuilder(inputLayer, outputLayer):
    net = tflearn.input_data(shape=[None, inputLayer])
    net = tflearn.fully_connected(net, int(inputLayer * .75))#, activation="sigmoid")
#    need to expand dimensions to use max pool
    #net = tf.expand_dims(net, 2)
    #net = max_pool_1d(net, int(inputLayer * .6))

    net = tflearn.fully_connected(net, int(inputLayer * .5))#, activation="sigmoid")

    net = tflearn.fully_connected(net, int(inputLayer * .25))#, activation="sigmoid")
    net = tflearn.fully_connected(net, outputLayer, activation='softmax')
    net = tflearn.regression(net)#, loss='softmax_categorical_crossentropy')
    model = tflearn.DNN(net, tensorboard_verbose=3)
    return model


def modelcnn(inputLayer, outputLayer):
	network = tflearn.input_data(shape=[None, inputLayer], name='input')
	network = tflearn.embedding(network, input_dim=inputLayer, output_dim=outputLayer)
	branch1 = conv_1d(network, int(inputLayer * .15), 3)#, padding='valid', activation='relu', regularizer="L2")
	branch2 = conv_1d(network, int(inputLayer * .15), 4)#, padding='valid', activation='relu', regularizer="L2")
	branch3 = conv_1d(network, int(inputLayer * .15), 5)#, padding='valid', activation='relu', regularizer="L2")
	network = merge([branch1, branch2, branch3], mode='concat', axis=1)
	network = tf.expand_dims(network, 2)
	network = global_max_pool(network)
	network = tflearn.dropout(network, 0.5)
	network = tflearn.fully_connected(network, outputLayer, activation='softmax')
	network = tflearn.regression(network, optimizer='adam', learning_rate=0.001,
                     loss='categorical_crossentropy', name='target')
# Training
	model = tflearn.DNN(network, tensorboard_verbose=3)
	return model

def encodeAndTrain(tfidfs, poss, labels, epochs, tfidfencoder, posencoder, batch=50):
    tfidfencodings = [tfidfencoder.predict(np.array([tfidf])).tolist()[0] for tfidf in tfidfs]
    posencodings = [posencoder.predict(np.array([pos])).tolist()[0] for pos in poss]
   # newTensors = [np.append(tfidfencodings[i], (poss[i])) for i in range(len(tfidfencodings))]
    #newTensors = [np.append(tfidfs[i], (poss[i])) for i in range(len(tfidfencodings))]
    newTensors = [np.array(tfidfs[i]) for i in range(len(tfidfencodings))]

    print len(tfidfencodings[1])
   # model = modelBuilder(len(tfidfencodings[1]) + len(poss[0]), 10)
   # model = modelBuilder(len(tfidfs[0]) + len(poss[0]), 10)
    tf.reset_default_graph()

    model = modelBuilder(len(tfidfs[0]), 10)
    model.fit(np.array(newTensors), labels, n_epoch=epochs, show_metric=True, batch_size=batch)
    return model
