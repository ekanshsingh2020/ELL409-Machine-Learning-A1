# -*- coding: utf-8 -*-
"""p1s6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RUkg-x1kjsWRhjGfTg8jcFMLhV1CKjmS
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

dataset1 = pd.read_csv('train.csv')
X_train = dataset1.iloc[ : , :-1].values
y_train = dataset1.iloc[:,-1].values
dataset2 = pd.read_csv('test.csv')
X_test = dataset2.iloc[ : , :-1].values
y_test = dataset2.iloc[:,-1].values

def get_mean(x):
    return np.sum(x,axis=0)/x.shape[0]

def get_std(x):
    return np.std(x,axis =0)

def get_standardized_data(x):
    x_mean = get_mean(x)
    x_dif = x-x_mean
    sigma = get_std(x)
    return x_dif

def expected_value(x):
  return np.sum(x,axis=0)/x.shape[0]

def get_min(X):
  return X.min(axis = 0)

def get_max(X):
  return X.max(axis = 0)

def get_normalized_data(X):
    X_std = (X - get_min(X_train)) / (get_max(X_train) - get_min(X_train))
    return X_std

import random
def stochastic_gradient_descent(x,y,epochs,learning_rate):
    number_of_features = x.shape[1]
    number_of_samples = x.shape[0]
    norm_x = get_normalized_data(x)
    initial_bias = np.ones((number_of_samples,1))
    norm_x = np.hstack((np.ones((number_of_samples,1)), norm_x))
    w = np.zeros(shape = (number_of_features+1))
    cost_list = []
    epoch_list = []
    for epoch in range(epochs):
      random_index = random.randint(0,number_of_samples-1)
      x_sample = norm_x[random_index]
      y_predicted = np.matmul(x_sample.T,w)
      dif = y[random_index] - y_predicted
      cost = np.mean(dif**2)/2
      w = w + (learning_rate)*(x_sample * dif)
      cost_list.append(cost)
      epoch_list.append(epoch)
    return w,cost_list,epoch_list

w,cost_list,epoch_list = stochastic_gradient_descent(X_train,y_train,100000,0.1)

print(w)

plt.xlabel("epoch")
plt.ylabel("cost")
plt.plot(epoch_list,cost_list)

def check_test_SGD(w,test,y_test):
  norm_x = get_normalized_data(test)
  number_of_samples = test.shape[0]
  norm_x = np.hstack((np.ones((number_of_samples,1)), norm_x))
  y_predicted = np.matmul(norm_x,w)
  error = y_test - y_predicted
  error = error/(len(y_test))
  print(error.shape)
  return error

error = check_test_SGD(w,X_test,y_test)

print(np.mean(error))

def get_variance(error):
  error_squared = np.square(error)
  return np.mean(error_squared)-np.mean(error)

get_variance(error)