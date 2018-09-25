import numpy as np
import tflearn

#input size of input and ouput layer to generate a autoEncoder to reduce input by 60%
def autoEncoder(inputLayer, outputLayer):
    # Encoder section
    encoder = tflearn.input_data(shape=[None, inputLayer])
    encoder = tflearn.fully_connected(encoder, int(inputLayer * .6))
    encoder = tflearn.fully_connected(encoder, int(inputLayer * .4))

    # Building the decoder
    decoder = tflearn.fully_connected(encoder, int(inputLayer * .6))
    decoder = tflearn.fully_connected(decoder, inputLayer, activation='sigmoid')

    #Decoder
    # Regression, with mean square error
    net = tflearn.regression(decoder, optimizer='adam', learning_rate=0.001,
                             loss='mean_square', metric=None)
    model = tflearn.DNN(net, tensorboard_verbose=3)
    encoder = tflearn.DNN(encoder)

    return model, encoder

#Input the decoder and encoder section of the intial model along with input data to train both
def trainEncoder(X, model, encoder):
    # Training model will train the encoder in effect
    print "x shape: ", X.shape
    model.fit(X, X, n_epoch=20, run_id="auto_encoder", batch_size=256, show_metric=True)
    return model
