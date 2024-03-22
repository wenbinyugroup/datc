import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score


# read path of .dat from TXT
with open("ML_filename.txt") as sd_lines:
    sd = sd_lines.readlines()
sd_name = sd[0].split('\n')[0].replace('\\','/')

predicted = np.load(sd_name+'pred_ML.npy')
y_true = np.load(sd_name+'true_ML.npy')

min_v = predicted.min(0)
max_v = predicted.max(0)

rsquare = round(r2_score(y_true, predicted), 3)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
plt.plot([min_v,max_v], [min_v,max_v], '-r')
plt.scatter(y_true, predicted)
ax.set_aspect('equal', adjustable='box')

plt.xlabel('True', fontsize = 25)
plt.ylabel('Prediction', fontsize =25)
plt.title('R square value is: ' + str(rsquare), fontsize =25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()