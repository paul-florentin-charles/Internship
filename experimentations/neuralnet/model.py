# -*- coding: utf-8 -*-

import parser._toml as ptml

from keras.models import Sequential
from keras.layers import Conv1D

def _init():
    model = Sequential()
    model.add(Dense(ptml.value('audio','s_len'), input_dim=ptml.value('audio','s_len')))
    #model.add(Conv1D(16, ptml.value('audio', 'frame_size'), strides=ptml.value('audio', 'hop_size'), input_dim=ptml.value('audio','s_len')))
    return model

def _compile(model):
    model.compile(ptml.value('neuralnet', 'optimizer'), ptml.value('neuralnet', 'loss'), ['accuracy'])

def _train(model, data, labels):
    model.fit(data, labels, ptml.value('neuralnet', 'batch_size'), ptml.value('neuralnet', 'epochs'))

def _predict(model, data):
    return model.predict(data, ptml.value('neuralnet', 'batch_size'))

def _evaluate(model, data, labels):
    return model.evaluate(data, labels, ptml.value('neuralnet', 'batch_size'))
