import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from keras.src.backend.jax.random import dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, BatchNormalization,Input
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
import Funcion_Deep as fd
import h5py
import random
from sklearn.metrics import classification_report
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.layers import LeakyReLU, BatchNormalization, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Sequential
from keras.metrics import AUC
from keras.callbacks import ReduceLROnPlateau

from sklearn.metrics import confusion_matrix

#first model architecture
def nn_model_1(Number_layers, nodos, activation_functions, in_s, loss_, optimizer_, learning_rate_, metrics_):
    model = Sequential()
    model.add(Input(shape=(in_s,)))  # Explicit Input layer

    # Add hidden layers dynamically
    for i in range(Number_layers):
        if activation_functions[i] == "leakyrelu":
            model.add(LeakyReLU(negative_slope=0.1))  #  Apply LeakyReLU separately
        else:
            model.add(Dense(nodos[i], activation=activation_functions[i]))  # Apply standard activations

    # Compile the model
    model.compile(
        loss=loss_,
        optimizer=optimizer_(learning_rate=learning_rate_),
        metrics=metrics_
    )

    return model

#second model architecture

def nn_model_2(Number_layers, nodos, activation_functions, in_s, loss_, optimizer_, learning_rate_, metrics_, Drop_Out_Layer=False, rate=0.2, BatchNorm_Layer=False):
    # this function is in order to use batch norm and drop out layer
    model = Sequential()
    model.add(Input(shape=(in_s,)))  #  Input Layer

    #  Hidden Layers with Optional BatchNormalization and Dropout
    for i in range(Number_layers - 1):  # Exclude output layer
        model.add(Dense(nodos[i]))  # No activation inside Dense

    if BatchNorm_Layer:
        model.add(BatchNormalization())  #  Normalize before activation

    model.add(Activation(activation_functions[i]))  #  Apply activation after BatchNorm

    if Drop_Out_Layer:
        model.add(Dropout(rate))  #  Dropout applied after activation

    #  Output Layer (No Dropout or BatchNorm)
    model.add(Dense(nodos[-1], activation=activation_functions[-1]))

    #  Compile the model
    model.compile(
        loss=loss_,
        optimizer=optimizer_(learning_rate=learning_rate_),
        metrics=metrics_
    )

    return model



def metrics_score(actual, predicted):
    """
    Function to print classification report and confusion matrix heatmap.
    """

    #  Print classification report
    print(classification_report(actual, predicted))

    # Compute confusion matrix
    cm = confusion_matrix(actual, predicted)

    plt.figure(figsize=(8, 5))

    #  Define class names list
    class_names_list = [str(i) for i in range(2)]  # Modify if necessary for different datasets

    #  Use class_names_list to label heatmap
    sns.heatmap(cm, annot=True, fmt='.0f', xticklabels=class_names_list, yticklabels=class_names_list, cmap="Blues")

    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title("Confusion Matrix")
    plt.show()