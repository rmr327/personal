from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import matplotlib.pyplot as plt


file_template = '/home/rmr327/Downloads/Inverted_Parallelogram_Test00{}.csv'  # Replace with path
data = pd.DataFrame()

for j in range(1, 4):
    df = pd.read_csv(file_template.format(j))
    df = (df - df.mean()) / df.std()
    data = pd.concat([data, df])

data = data[['Relative Time', 'Absolute Energy (FX) ', 'Peak Frequency (FX)  ', 'Signal Strength (FX) ',
             'Reverberation Frequency (FX) ', 'Counts (FX)          ']]

y = pd.read_csv('/home/rmr327/Downloads/Inverted_Parallelogram_4mm_Test001 (1).csv')  # Just for time labels
x = pd.read_csv('/home/rmr327/Downloads/Inverted_Parallelogram_4mm_Test001.csv')  # for plotting

cluster = AgglomerativeClustering(n_clusters=6, affinity='cosine', linkage='average')

cluster.fit_predict(data)

fig, axs = plt.subplots(2, 2)

labels = cluster.labels_[0:526]

plt_one = axs[0, 0].scatter(y['Time (*)             '], y['Counts               '], c=labels, cmap='Spectral')
plt_two = axs[0, 1].scatter(y['Time (*)             '], y['Reverberation Frequency (FX) '], c=labels, cmap='Spectral')
plt_three = axs[1, 0].scatter(y['Time (*)             '], y['Signal Strength (FX) '], c=labels,
                              cmap='Spectral')
plt_four = axs[1, 1].scatter(y['Time (*)             '], y['Peak Frequency (FX)  '], c=labels, cmap='Spectral')

y_labels = ['Absolute Energy (FX)', 'Amplitude (FX)', 'Signal Strength (FX)', 'Peak Frequency (FX)']
plots = [plt_one, plt_two, plt_three, plt_four]
axes = axs.flat

for i in range(len(axes)):
    axes[i].set(xlabel='Time (sec)')
    # axes[i].label_outer()
    axes[i].set(ylabel=y_labels[i])
    fig.colorbar(plots[i], ax=axes[i])


plt.show()

"""
# Uncomment if you want to save labels
# Lets save our labels
for j in range(1, 4):
    df = pd.read_csv(file_template.format(j))
    cluster.fit_predict(df)
    df['clustering_labels'] = cluster.labels_
    df.to_csv(file_template.format('{}_with_labels'.format(j)))
"""