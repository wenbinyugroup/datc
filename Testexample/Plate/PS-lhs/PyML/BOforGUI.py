import numpy as np
import pandas as pd
from pyDOE import *
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import cross_val_score
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, Dropout
# from keras.optimizer_v1 import Adam, SGD, RMSprop, Adadelta, Adagrad, Adamax, Nadam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from scikeras.wrappers import KerasRegressor
from math import floor
from sklearn.metrics import make_scorer, r2_score
from bayes_opt import BayesianOptimization
from sklearn.model_selection import StratifiedKFold, KFold
from keras.layers import LeakyReLU
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],[tf.config.experimental.VirtualDeviceConfiguration(memory_limit=5120)])
  except RuntimeError as e:
    print(e)

# from tensorflow.keras.optimizers import Adam
LeakyReLU = LeakyReLU(alpha=0.1)
import warnings
warnings.filterwarnings('ignore')
pd.set_option("display.max_columns", None)

# Make scorer accuracy
score_acc = make_scorer(r2_score)

def r_squared(y, y_hat):
    y_bar = y.mean()
    ss_tot = ((y - y_bar) ** 2).sum()
    ss_res = ((y - y_hat) ** 2).sum()
    return 1 - (ss_res / ss_tot)

#####################################################
################  Read data from files ##############
#####################################################

x_lf = []
y_lf = []
bo_paras = []
with open('ML_filename.txt') as sd:
    lines_sd = sd.readlines()
sdname = lines_sd[0].split()[0]

with open(sdname+'BOparas.txt') as bo:
    lines_bo = bo.readlines()
for i in range(0, len(lines_bo)):
    line3 = lines_bo[i].split()
    bo_paras.append(line3)
############## data from Latin hypercube sampling (LHS)
with open(sdname) as inp:
    lines_lf = inp.readlines()

x_lf = []
y_lf = []

for i in range(1,len(lines_lf)):
    line1 = lines_lf[i].split()
    input_list = []
    for j in range(2, len(line1)-1):
        input_list.append(float(line1[j])/90)
    x_lf.append(input_list)
    y_lf.append([float(line1[-1])])

###############################################################################################################################################################x_lf = np.array(x_lf)
x_lf = np.array(x_lf)
y_lf = np.array(y_lf)

y_min = min(y_lf).tolist()
y_max = max(y_lf).tolist()

y_lf = (y_lf - y_min[0])/ (y_max[0] - y_min[0])



y_lf = np.reshape(y_lf, (len(y_lf),1))

x_train, x_rem, y_train, y_rem = train_test_split(x_lf, y_lf, train_size=0.8, random_state=0)
x_val, x_test, y_val, y_test = train_test_split(x_rem, y_rem, test_size=0.5, random_state=0)
# x_train = x_lf
# y_train = y_lf
def nn_cl_bo(neurons, activation, learning_rate,  batch_size, epochs, dropout, nlayers):
    activationL = ['relu', 'sigmoid', 'softplus', 'softsign', 'tanh', 'selu',
                   'elu', 'exponential', LeakyReLU]
    neurons = round(neurons)
    activation = activationL[round(activation)]
    batch_size = round(batch_size)
    epochs = round(epochs)
    nlayers = round(nlayers)

    opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    nn = Sequential()
    nn.add(Dense(neurons, input_dim=np.shape(x_lf)[-1], activation=activation))
    nn.add(Dropout(dropout))
    for i in range(nlayers):
        nn.add(Dense(neurons, activation=activation))
        nn.add(Dropout(dropout))
    nn.add(Dense(1, activation='relu'))
    nn.compile(loss='mse', optimizer=opt)
    es = EarlyStopping(monitor='loss', mode='min', verbose=0, patience=20)
    nn.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=epochs, verbose=0, batch_size=batch_size, callbacks=es)
    ypred = nn.predict(x_lf, verbose=0)
    # print('*'*23)
    # print(np.shape(ypred))
    # print(np.shape(y_test))
    # print('*'*23)
    score = r_squared(np.array(y_lf), np.array(ypred))
    score = np.nan_to_num(score)

    return score

# Set paramaters
params_nn ={
    'neurons': (50, 500),
    'activation':(0, 8),
    'learning_rate':(1e-10, 1e-2),
    'batch_size':(50, 512),
    'epochs':(100, 1000),
    'dropout':(0, 0.8),
    'nlayers':(1, 20)
}
# Run Bayesian Optimization
import time
start_time = time.time()
nn_bo = BayesianOptimization(nn_cl_bo, params_nn, random_state=123)
nn_bo.maximize(init_points=int(bo_paras[0][0]), n_iter=int(bo_paras[1][0]))
# nn_bo.max['target']
end_time = time.time()
print("---Bayesian optimization time =  %s seconds ---" % (end_time - start_time))
print(nn_bo.max)

##########################################################################################
###   use bo result to train model and predict

activationL = ['relu', 'sigmoid', 'softplus', 'softsign', 'tanh', 'selu',
                   'elu', 'exponential', LeakyReLU]
neurons_bo = round(nn_bo.max['params']['neurons'])
activation_bo = activationL[round(nn_bo.max['params']['activation'])]
batch_size_bo = round(nn_bo.max['params']['batch_size'])
epochs_bo = round(nn_bo.max['params']['epochs'])
nlayers_bo = round(nn_bo.max['params']['nlayers'])

opt_bo = tf.keras.optimizers.Adam(learning_rate = nn_bo.max['params']['learning_rate'])
nn_bomodel = Sequential()
nn_bomodel.add(Dense(neurons_bo, input_dim=np.shape(x_lf)[-1], activation=activation_bo))
nn_bomodel.add(Dropout(nn_bo.max['params']['dropout']))
for i in range(nlayers_bo):
    nn_bomodel.add(Dense(neurons_bo, activation=activation_bo))
    nn_bomodel.add(Dropout(nn_bo.max['params']['dropout']))
nn_bomodel.add(Dense(1, activation='relu'))
nn_bomodel.compile(loss='mse', optimizer=opt_bo)


history = nn_bomodel.fit(x_train, y_train, validation_data = (x_val, y_val), epochs=epochs_bo, batch_size=batch_size_bo, verbose=1)


import matplotlib.pyplot as plt
import matplotlib
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 25}

matplotlib.rc('font', **font)

plt.figure(figsize=(12,8))
plt.plot(history.history['loss'],linewidth=3.0)
plt.plot(history.history['val_loss'],linewidth=3.0)
# plt.title('model accuracy')
plt.ylabel('Loss Value', fontsize=30)
plt.xlabel('Epoch', fontsize=30)
plt.legend(['Train_loss', 'Val_loss'], loc='center right', fontsize=30)
plt.grid(True)
plt.show()

predicted = nn_bomodel.predict(x_lf, verbose=0)

min_v = predicted.min(0)
max_v = predicted.max(0)


fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
plt.plot([min_v,max_v], [min_v,max_v], '-r')
plt.scatter(y_lf, predicted)
ax.set_aspect('equal', adjustable='box')
plt.xlabel('True', fontsize = 25)
plt.ylabel('Prediction', fontsize = 25)
plt.grid(True)
plt.tight_layout()
plt.show()

print(r_squared(y_lf, predicted))