#!/usr/bin/env python

#mlp_model_api.py
#
#by Joe Hahn
#joe.hahn@oracle.com
#12 July 2018
#
#this api uses the mlp model to classify (x,y) input data, and returns predicted class X,O, or B
#
#example usage:
#    from mlp_model_api import *
#    data = {"x":1.0, "y":2.0}
#    api_predict(data)

#load mlp model
from keras.models import load_model
model = load_model('mlp_model.h5')

#model api
def api_predict(data):
    
    #convert input data dict to numpy array
    xx = float(data['x'])
    yy =  float(data['y'])
    data_list = [ [xx, yy], ]
    from numpy import array
    x = array(data_list)
    
    #compute predicted class probability
    y = model.predict(x)[0]
    y = y/y.sum()
    
    #select highest-scoring class
    y_cols = ['O_score', 'X_score', 'B_score']
    idx = y.argmax()
    class_prob = y[idx]
    class_pred = y_cols[idx][0]
    
    #return result as dict aka json
    y_json = {'class_pred':class_pred, 'class_prob':class_prob}
    return y_json
