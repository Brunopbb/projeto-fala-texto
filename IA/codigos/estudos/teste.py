import numpy as np
import random


training_data = [
    (np.array([[0.1], [0.9]]), np.array([[1]])),
    (np.array([[0.8], [0.2]]), np.array([[0]])),
    (np.array([[0.4], [0.6]]), np.array([[1]])),
    (np.array([[0.7], [0.3]]), np.array([[0]]))
]

mini_batche_size = 2
epochs = 1
n = len(training_data)
training_data = list(training_data)

for j in range(epochs):
    random.shuffle(training_data)
    mini_batches = [training_data[k:k+mini_batche_size] for k in range(0, n, mini_batche_size)]




print(mini_batches)