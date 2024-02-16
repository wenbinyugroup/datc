# Import python libraries required in this example:
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from sklearn.model_selection import train_test_split
import numpy as np
import scipy
import tensorflow as tf
from sklearn.preprocessing import normalize
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],[tf.config.experimental.VirtualDeviceConfiguration(memory_limit=5120)])
  except RuntimeError as e:
    print(e)

# read path of .dat from TXT
with open("ML_filename.txt") as sd_lines:
    sd = sd_lines.readlines()
sd_name = sd[0].split('\n')[0].replace('\\','/')

# read training parameters from TXT
with open(sd_name+"ML_paras.txt") as ml_lines:
    ml = ml_lines.readlines()

ml_struct = list()
ml_struct_list = ml[0].split('\n')[0].replace('[','').replace(']','').strip().split(',')
for i in ml_struct_list:
    ml_struct.append(int(i))

ml_optimizer = ml[1].split('\n')[0]
ml_lr = ml[2].split('\n')[0]
ml_epoch = ml[3].split('\n')[0]
# read data from .dat files
# with open("sq_plate_tailorable_expr_samp_lhs_tabular_40x40.dat") as inp:
    # lines_hf = inp.readlines()
# with open("sq_plate_tailorable_expr_samp_lhs_tabular_10x10.dat") as inp:
#     lines_lf = inp.readlines()
with open(sd_name) as inp:
    lines_hf = inp.readlines()

# x_lf = []
# y_lf = []
x_hf = []
y_hf = []
for i in range(1,len(lines_hf)):
    line1 = lines_hf[i].split()
    input_list = []
    for j in range(2, len(line1)-1):
        input_list.append(float(line1[j])/90)
    x_hf.append(input_list)
    y_hf.append([float(line1[-1])])

x_hf = np.array(x_hf)
y_hf = np.array(y_hf)

# normalize output
y_hf = (y_hf - y_hf.min())/(y_hf.max() - y_hf.min())


x_train, x_rem, y_train, y_rem = train_test_split(x_hf, y_hf, train_size=0.8, random_state=0)
x_val, x_test, y_val, y_test = train_test_split(x_rem, y_rem, test_size=0.5, random_state=0)

# Define the network model and its arguments.
# Set the number of neurons/nodes for each layer:
model = Sequential()
model.add(Dense(ml_struct[0], input_shape=(np.shape(x_hf)[-1],)))
model.add(Activation('relu'))
for j in ml_struct[1:-1]:
    model.add(Dense(j))
    model.add(Activation('relu'))
model.add(Dense(ml_struct[-1]))
model.add(Activation('relu'))

# Compile the model and calculate its accuracy:
Optimizer = tf.keras.optimizers.Adam(learning_rate=float(ml_lr), decay=1e-6)

model.compile(loss='mean_squared_error', optimizer=Optimizer, metrics=['accuracy'])

# Print a summary of the Keras model:
# model.summary()
history = model.fit(x_train, y_train, validation_data = (x_val, y_val), epochs=int(ml_epoch), batch_size=100)


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
plt.tight_layout()
plt.show()


# y_true = []
# y_true_id = []
# predicted = model.predict(x_test)
# for i in x_test:
#     for j in range(len(x_hf)):
#         if x_hf[j].tolist() == i.tolist():
#             y_true_id.append(j)
#
# for k in y_true_id:
#     y_true.append(y_hf[k])
#
# # save prediction and true values for Testing plot use
# np.save('pred_ML.npy', predicted)
# np.save('true_ML.npy', y_true)


y_true = y_test
predicted = model.predict(x_test)
min_v = predicted.min(0)
max_v = predicted.max(0)


# save prediction and true values for Testing plot use
np.save(sd_name+'pred_ML.npy', predicted)
np.save(sd_name+'true_ML.npy', y_true)


# fig = plt.figure(figsize=(8,8))
# ax = fig.add_subplot(111)
# plt.plot([min_v,max_v], [min_v,max_v], '-r')
# plt.scatter(y_true, predicted)
# ax.set_aspect('equal', adjustable='box')
# plt.xlabel('True', fontsize = 25)
# plt.ylabel('Prediction', fontsize = 25)
# plt.grid(True)
# plt.tight_layout()
# plt.show()
