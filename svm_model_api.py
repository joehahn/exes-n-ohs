#!/usr/bin/env python

#svm_model_api.py
#
#by Joe Hahn
#joe.hahn@oracle.com
#13 July 2018
#
#this api uses the svm model to classify (x,y) input data, and returns predicted class X,O, or B
#
#example usage:
#    from svm_model_api import *
#    data = {"x":1.0, "y":2.0}
#    api_predict(data)

#load svm model
import pickle as pkl
model = pkl.load(open('svm_model.pkl', 'rb'))

#model api
def api_predict(data):
    
    #convert input data dict to numpy array
    x0 = float(data['x'])
    x1 =  float(data['y'])
    data_list = [ [x0, x1], ]
    from numpy import array
    x = array(data_list)
    
    #compute predicted class
    y = model.predict(x)[0]

    #return result as dict aka json
    y_dict = {'class_pred':y}
    return y_dict
