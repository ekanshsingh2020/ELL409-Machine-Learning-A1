# -*- coding: utf-8 -*-
"""p1s3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JxtoCUrvIqJmvHi_blCYisuVx-KrEwcX
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

print(X_train.shape)

print(y_train.shape)

print(X_test.shape)

print(y_test.shape)

"""**Standardization of Data**"""

# Standard Scaling
def get_mean(x):
    return np.sum(x,axis=0)/x.shape[0]

def get_std(x):
    return np.std(x,axis =0)

def get_standardized_data(x):
    x_mean = get_mean(x)
    x_dif = x-x_mean
    sigma = get_std(x)
    return x_dif

X_train_standardized = get_standardized_data(X_train)

X_test_standardized = get_standardized_data(X_test)

print(X_test)

print(X_test_standardized)

"""**Normalization of Data**"""

def get_min(X):
  return X.min(axis = 0)

def get_max(X):
  return X.max(axis = 0)

def get_normalized_data(X):
    X_std = (X - get_min(X_train)) / (get_max(X_train) - get_min(X_train))
    return X_std

X_train_normalized = get_normalized_data(X_train)

print(X_train)

print(X_train_normalized)

X_test_normalized = get_normalized_data(X_test)

print(X_test)

print(X_test_normalized)

"""**Stochastic Gradient Descent**"""

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

w_SGD,cost_list_SGD,epoch_list_SGD = stochastic_gradient_descent(X_train,y_train,100000,0.01)

print(w_SGD)

plt.xlabel("epoch")
plt.ylabel("cost")
plt.plot(epoch_list_SGD,cost_list_SGD)

def check_test_SGD(w,test,y_test):
  norm_x = get_normalized_data(test)
  number_of_samples = test.shape[0]
  norm_x = np.hstack((np.ones((number_of_samples,1)), norm_x))
  y_predicted = np.matmul(norm_x,w)
  error = y_test - y_predicted
  error = error/(len(y_test))
  return error

error_SGD = check_test_SGD(w_SGD,X_test,y_test)

print(np.mean(error_SGD))

"""**Lasso Regression**"""

import random
def lasso_regression(x,y,epochs,penality,learning_rate):

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
      cost += abs(w)*penality
      w_grad = penality + (x_sample * dif)
      w = w + (learning_rate)*w_grad
      cost_list.append(cost)
      epoch_list.append(epoch)
    return w,cost_list,epoch_list

w_lasso,cost_list_lasso,epoch_list_lasso = lasso_regression(X_train,y_train,100000,0.1,0.01)

w_lasso

plt.xlabel("epoch")
plt.ylabel("cost")
plt.plot(epoch_list_lasso,cost_list_lasso)

def check_test_lasso(w,test,y_test):
  norm_x = get_normalized_data(test)
  number_of_samples = test.shape[0]
  norm_x = np.hstack((np.ones((number_of_samples,1)), norm_x))
  y_predicted = np.matmul(norm_x,w)
  error = y_test - y_predicted
  error = error/(len(y_test))
  return error

error_lasso = check_test_lasso(w_lasso,X_test,y_test)

print(np.mean(error_lasso))

"""**Ridge Regression**"""

import random
def ridge_regression(x,y,epochs,penality,learning_rate):
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
      #cost = np.mean(dif**2)/2 + penality*(np.matmul(w,w.T))
      cost = np.mean(dif**2)/2 + penality*(np.sum(np.square(w)))
      w_grad = x_sample * dif + w*penality
      w = w + (learning_rate)*w_grad
      cost_list.append(cost)
      epoch_list.append(epoch)
    return w,cost_list,epoch_list

w_ridge,cost_list_ridge,epoch_list_ridge = ridge_regression(X_train,y_train,1000,0.001,0.1)

plt.xlabel("epoch")
plt.ylabel("cost")
plt.plot(epoch_list_ridge,cost_list_ridge)

def check_test_ridge(w,test,y_test):
  norm_x = get_normalized_data(test)
  number_of_samples = test.shape[0]
  norm_x = np.hstack((np.ones((number_of_samples,1)), norm_x))
  y_predicted = np.matmul(norm_x,w)
  error = y_test - y_predicted
  error = error/(len(y_test))
  return error

error_ridge = check_test_ridge(w_ridge,X_test,y_test)

print(np.mean(error_ridge))