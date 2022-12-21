# -*- coding: utf-8 -*-
"""p3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gFCTMOZQU4U9V9ArtmVkQhLOtqcOPYYi
"""

import numpy as np 
import gzip
import matplotlib.pyplot as plt

## Handle the necessary imports


## Function to read the data from the compressed files
def read_data():
    train_images = gzip.open('train-images-idx3-ubyte.gz','r')
    train_labels = gzip.open('train-labels-idx1-ubyte.gz','r')
    image_size = 28
    num_images = 60000
    train_images.read(16)
    buffer = train_images.read(image_size * image_size * num_images)
    data_train_image = np.frombuffer(buffer, dtype=np.uint8).astype(np.float32)
    data_train_image = data_train_image.reshape(num_images, image_size, image_size, 1)
    y = [] 
    train_labels.read(8)
    for i in range(num_images):   
        buf = train_labels.read(1)
        labels = np.frombuffer(buf, dtype=np.uint8).astype(np.int64)
        y.append(labels[0])
    y = np.array(y)
    X = []
    for i in data_train_image:
        xi = np.asarray(i).squeeze()
        X.append(xi.flatten())
    X = np.array(X)
    return X, y

## Function to get subset of data with labels 2 and 9
def get_subset(X, y):
    indices = np.where((y == 2) | (y == 9))
    X_subset = X[indices]
    y_subset = y[indices]
    return X_subset, y_subset

## In case you need the whole data, use this:
X, y = read_data()

## In case you need the subset of data with classes 2 and 9 use this:
X_subset, y_subset = get_subset(X, y)

np.save("train_images_subset.npy", X_subset)
np.save("train_labels_subset.npy", y_subset)

np.save("train_images.npy", X)
np.save("train_labels.npy", y)

X,y=read_data()
print(X.shape,y.shape)

#diaplaying random example from dataset
img_dim=int(np.sqrt(X.shape[1]))
def display_example():
    ind = np.random.randint(X.shape[0]) #random index
    img = X[ind].reshape(img_dim,img_dim)
    print(img)
    print("Number is:", y[ind])
    plt.imshow(img)
display_example()

def normalize_X(data):
    mean = np.mean(data, axis=1, keepdims=True)

    std = np.std(data, axis=1, keepdims=True)
    normalized_data = (data - mean)/std
    return normalized_data

X=normalize_X(X)

one_hot_y = np.zeros((y.size, y.max()+1))
one_hot_y[np.arange(y.size),y] = 1
Y=one_hot_y
print(Y.shape)

shuffler = np.random.permutation(X.shape[0]) #shuffling dataset
X = X[shuffler]
Y = Y[shuffler]
y=y[shuffler]

X_train=X[:int(X.shape[0]*0.8),:].T
Y_train=Y.reshape(Y.shape[0],10)[:int(Y.shape[0]*0.8),:].T
y_train=y.reshape(y.shape[0],1)[:int(y.shape[0]*0.8),:].T
X_test=X[int(X.shape[0]*0.8):,:].T
Y_test=Y.reshape(Y.shape[0],10)[int(Y.shape[0]*0.8):,:].T
y_test=y.reshape(y.shape[0],1)[int(Y.shape[0]*0.8):,:].T
print("Shape of X_train: "+str(X_train.shape))
print("Shape of Y_train: "+str(Y_train.shape))
print("Shape of X_test: "+str(X_test.shape))
print("Shape of Y_test: "+str(Y_test.shape))
print("Shape of y_test: "+str(y_test.shape))

def sigmoid(z):
    s = 1/(1+np.exp(-z))
    return s

def initialize_zero_parameters(dim):

    w = np.zeros((dim,10))
    b = 0
    return w, b

def forward_and_backward_propagate(w, b, X, Y):  
    m = X.shape[1]
    
    # Forward propagation
    A = sigmoid(np.dot(w.T,X) + b)              # computing activation
    cost = np.sum(((- np.log(A))*Y + (-np.log(1-A))*(1-Y)))/m  # computing cost
  
    # Backward propagation

    dw = (np.dot(X,(A-Y).T))/m
    db = (np.sum(A-Y))/m

    cost = np.squeeze(cost)

    grads = {"dw": dw,
             "db": db}
    
    return grads, cost

def iteration(w, b, X, Y, num_iterations, learning_rate):
    costs = []
    
    for i in range(num_iterations):
        
        
        # Cost and gradient calculation 
        grads, cost = forward_and_backward_propagate(w, b, X, Y)

        dw = grads["dw"]
        db = grads["db"]
        
        # updating parameters
 
        w = w - (learning_rate*dw)
        b = b - (learning_rate*db)

        # Record the costs
        if i % 100 == 0:
            costs.append(cost)
    params = {"w": w,
              "b": b}
    
    grads = {"dw": dw,
             "db": db}
    
    return params, grads, costs

def prediction(w, b, X):
    m = X.shape[1]
    Y_prediction = np.zeros((10,m))
    w = w.reshape(X.shape[0], 10)
    
    A = sigmoid(np.dot(w.T,X) + b)           # Dimension = (10, m)
    for i in range(m):
      ind=list(A[:,i]).index(max(list(A[:,i])))
      Y_prediction[ind,i]=1

    return Y_prediction

def model(X_train, Y_train, X_test, Y_test, num_iterations, learning_rate = 0.01):
    
    # initialize parameters with zeros 
    w, b = initialize_zero_parameters(X_train.shape[0])

    # Gradient descent
    parameters, grads, costs = iteration(w, b, X_train, Y_train, num_iterations, learning_rate)
    
    # obtaining trained parameters
    w = parameters["w"]
    b = parameters["b"]
    
    # prediction of model on train and test data set
    Y_prediction_test = prediction(w, b, X_test)
    Y_prediction_train = prediction(w, b, X_train)


    #print("train accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_train - Y_train)) * 100))
    #print("test accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_test - Y_test)) * 100))
    print("Model is trained")
    
    d = {"costs": costs,
         "Y_prediction_test": Y_prediction_test, 
         "Y_prediction_train" : Y_prediction_train, 
         "w" : w, 
         "b" : b,
         "learning_rate" : learning_rate,
         "num_iterations": num_iterations}
    
    return d

d = model(X_train, Y_train, X_test,Y_test, 300, learning_rate = 0.01)

correct_train=0
correct_test=0
for i in range(Y_test.shape[1]):
  ind1=np.where(d["Y_prediction_test"][:,i].reshape(10,1).T[0]==1)[0][0]
  ind2=np.where(Y_test[:,i].reshape(10,1).T[0]==1)[0][0]
  if(ind1==ind2):
    correct_test+=1
for i in range(Y_train.shape[1]):
  ind1=np.where(d["Y_prediction_train"][:,i].reshape(10,1).T[0]==1)[0][0]
  ind2=np.where(Y_train[:,i].reshape(10,1).T[0]==1)[0][0]
  if(ind1==ind2):
    correct_train+=1
print("train accuracy: " +str(correct_train*100/Y_train.shape[1])+"%")
print("test accuracy: "+str(correct_test*100/Y_test.shape[1])+"%")

costs = np.squeeze(d['costs'])
plt.plot(costs)
plt.ylabel('cost')
plt.xlabel('iterations')
plt.show()

#converting output hot encoding into labels

y_pred_test_label=np.zeros((1,Y_test.shape[1]))
for i in range(Y_test.shape[1]):
  ind=np.where(d["Y_prediction_test"][:,i].reshape(10,1).T[0]==1)[0][0]
  y_pred_test_label[0,i]=ind
y_target_test_label=np.zeros((1,Y_test.shape[1]))
for i in range(Y_test.shape[1]):
  ind=np.where(Y_test[:,i].reshape(10,1).T[0]==1)[0][0]
  y_target_test_label[0,i]=ind
print(y_pred_test_label)
print(y_target_test_label)

from sklearn.metrics import multilabel_confusion_matrix
conf_matrix = multilabel_confusion_matrix(y_true=y_target_test_label[0], y_pred=y_pred_test_label[0],labels=[0,1,2,3,4,5,6,7,8,9])
print(conf_matrix)