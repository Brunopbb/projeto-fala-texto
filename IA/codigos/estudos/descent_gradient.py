import numpy as np
import matplotlib.pyplot as plt


def predict(x, w0, w1):
    return w0 + w1*x


def MSE(X, y, w0, w1):

    cost = 0

    for feature, value in zip(X, y):
        cost += (predict(feature, w0, w1) - value) ** 2
    
    return cost/len(X)

def descent_gradient_step(X, y, w0, w1, alpha):
    
    error_w0 = 0
    error_w1 = 0

    for feature, value in zip(X, y):
        error_w0 += predict(feature, w0, w1) - value
        error_w1 += (predict(feature, w0, w1) - value) * feature

    new_w0 = w0 - alpha * (1/len(X)) * error_w0
    new_w1 = w1 - alpha * (1/len(X)) * error_w1

    return new_w0, new_w1

def descent_gradient(X, y, w0, w1, alpha, epochs):

    cost = np.zeros(epochs)

    for epoch in range(epochs):
        w0, w1 = descent_gradient_step(X, y, w0, w1, alpha)
        cost[epoch] = MSE(X, y, w0, w1) 

    return w0, w1, cost

X = np.array([0.5, 2.2, 2.0])
y = np.array([2.0, 2.5, 1.4])

alpha = 0.01
w0 = 0.1
w1 = 0.1
epochs = 850


n_w0, n_w1, cost = descent_gradient(X, y, w0, w1, alpha, epochs)

print("w0={}, w1={}".format(n_w0, n_w1))

print("predict={}".format(predict(1.5, n_w0, n_w1)))