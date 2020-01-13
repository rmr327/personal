import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv(r'C:\Users\rakee\PycharmProjects\personal\computing_and_controls\data_set.csv', header=None)
#  df = df.iloc[:26, :]

initial_y_pred = [5.0+x for x in range(16)]
# initial_y_pred = [5.0, 10.0, 15.0]
predicted_distance = pd.DataFrame([initial_y_pred])

alpha = 0.0824
# alpha = 0.7535
# alpha = 0.701001

for i in range(len(df)):
    # res = df.iloc[i].values + alpha*(predicted_distance.iloc[i].values - df.iloc[i].values)
    res = predicted_distance.iloc[i].values + alpha * (df.iloc[i].values - predicted_distance.iloc[i].values)
    predicted_distance = predicted_distance.append(pd.DataFrame([res]))


# predicted_distance.columns = [x+5 for x in range(20)]
# predicted_distance.columns = [5, 10, 15]
# predicted_distance.to_csv('predicted_data_1.csv', index=None)

# Lets process the standard deviation
std = np.std(df, ddof=1)
std_df = pd.DataFrame()

for i in range(len(std)):
    for j in range(len(df)):
        std_df[i] = [std[i] for yy in range(len(df))]

# averaging filter for comparison
avg = df.groupby(np.arange(len(df))//10).mean()
avg_df = pd.DataFrame(columns=df.columns)

count = 0
for v in avg.values:
    for j in range(10):
        avg_df.loc[count] = v
        count += 1

avg_df.to_csv('averaging_filter_for_part_1')

i = 8  # Which ground truth do you want to plot

# Lets plot
plt.plot(df.iloc[:, i], 'r')
predicted_distance.reset_index(inplace=True)
plt.plot(predicted_distance.iloc[:, i+1])
plt.plot(3*std_df[i]+(i*1)+5, 'k')
plt.plot((i*1)+5-3*std_df[i], 'g')
plt.plot(avg_df.iloc[:, i], 'm')
plt.xlabel('Sample Number')
plt.ylabel('Position/Inches')

plt.legend(['Measured Data', 'Alpha KF Filtered Data', '+ve X 3sigma', '-ve X 3sigma', 'Averaging Filter Data'])
plt.title('Position vs Number of Sample for ground truth = {}'.format(str((i*1)+5)))

plt.show()
