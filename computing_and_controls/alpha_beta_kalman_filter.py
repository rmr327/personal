import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


meas_df = pd.read_csv(r'C:\Users\rakee\PycharmProjects\personal\computing_and_controls\data_set.csv', header=None)
initial_x_pred = [5.0+x for x in range(16)]
initial_v_pred = [1.0+x for x in range(16)]
# pred_array = np.array([initial_x_pred, initial_v_pred])

x_df = pd.DataFrame(columns=[x+5 for x in range(16)])
v_df = pd.DataFrame(columns=[1 for x in range(16)])

meas_v = [1 for x in range(16)]

# beta = 0.22
# alpha = 0.32035

beta = 0.8840
alpha = 0.8876

x = [x+5 for x in range(16)]
v = [9 for u in range(16)]
pred_array = [x, v]

for i in range(len(meas_df)):
    pred_array = np.matmul(np.array([[1, 1], [0, 1]]), pred_array) + \
                 np.matmul(np.array([[alpha], [beta]]), (np.array([meas_df.loc[i].values]) -
                                                         np.matmul(np.array([1, 0]),
                                                                   np.matmul(np.array([[1, 1], [0, 1]]), pred_array))))

# plot 1
plt.plot(meas_df.loc[0], 'r.')
plt.plot(pred_array[0], 'g.')
plt.plot([r+5 for r in range(16)], 'bx')
plt.xlabel('Time/s')
plt.ylabel('Position/Inches')
plt.title('Position vs Time')

plt.legend(['Measured', 'Alpha-Beta KF Filtered', 'Ground truth'])

pred_array[1] = pred_array[1] + 1

# plot 2
mean_measured = meas_df.mean()
t = 1
velocity_measured = [(mean_measured[i+1] - mean_measured[i])/t for i in range(len(mean_measured)-1)]

# plt.plot(pred_array[1], 'g.')
# plt.plot([1 for i in range(16)], 'r.')
# plt.plot(velocity_measured, 'b.')
# plt.xlabel('Time/s')
# plt.ylabel('Velocity/(Inches/sec)')
# plt.title('Velocity vs Time')

# plt.legend(['Alpha-Beta KF Filtered', 'Ground truth', 'Measured'])

# plt.ylim([0, 2])

plt.show()
# for i in range(len(meas_df)):
#     pred_array = np.matmul(np.array([[1, 1], [0, 1]]), pred_array) + \
#                np.matmul(np.array([[alpha], [beta]]), (np.array([meas_df.loc[i].values]) - np.matmul(np.array([1, 0]),
#                                                                                                        pred_array)))
#

# x_df.loc[i] = pred_array[0]
# v_df.loc[i] = pred_array[1]
