import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import stats
import numpy as np


class KeyGen:
    def __init__(self, file_names):
        self.file_names = file_names
        self.node_1_df = None
        self.node_2_df = None
        self.node_1_start_time = None
        self.node_1_end_time = None

    @staticmethod
    def str_to_amp(num_str):
        output = []
        for element in num_str:
            try:
                output.append(20 * np.abs(np.log10(abs(complex(element)))))
            except ValueError:
                element = element.replace('+', '')
                output.append(20 * np.abs(np.log10(abs(complex(element)))))

        # an_val = np.mean(output)
        # std_val = np.std(output)
        # output = [(k - mean_val)/std_val for k in output]
        return output

    @staticmethod
    def extract_time(time_str):
        datetime_object = datetime.strptime(time_str[11:19], '%H:%M:%S')
        return datetime_object.time()

    def format_data(self):
        for i in range(2):
            df = pd.read_csv(self.file_names[i], header=None, sep=r'\t')
            df.rename(columns={0: 'time_stamp', 55: 'SNR', 54: 'signal', 53: 'Noise'}, inplace=True)
            # df = df.iloc[2000: 4000, :]
            df = df.loc[(df['signal'].astype(int) >= 13)]
            df['time_stamp'] = df['time_stamp'].astype(str).str[:-2]

            # df = df.loc[(df['SNR'] >= 10)]
            df = df.replace(r'\(', '', regex=True)
            df = df.replace(r'\)', 'j', regex=True)
            df = df.replace(',', '+', regex=True)
            df = df.apply(lambda x: self.str_to_amp(x.values) if x.name not in ['time_stamp', 'SNR'] else x)
            # subcarriers = list(range(1, 53))
            # z_score = np.abs(pd.DataFrame(stats.zscore(df[subcarriers])))
            # df[subcarriers] = z_score
            # df[subcarriers] = df[subcarriers].mask(df[subcarriers] > 7)
            # filt = z_score.loc[z_filt]
            # z_score.where(filt, inplace=True)
            print(df.head())

            # df = df.loc[(z_score < 2) & (z_score > 0)]
            df.reset_index(inplace=True, drop=True)

            # df['SNR'] = df['SNR'].abs()
            # min_snr = min(df['SNR'])
            # df['SNR'] = (df['SNR'] - min_snr) / (max(df['SNR']) - min_snr)  # Normalizing SNR
            min_vals = df.iloc[:, 1:53].min()
            # df.iloc[:, 1:53] = (df.iloc[:, 1:53] - min_vals) / (df.iloc[:, 1:53].max() - min_vals)  # Normalizing
            df['time_stamp'] = df['time_stamp'].astype(int)

            if i == 0:
                self.node_1_df = df
                self.node_1_start_time = int(df['time_stamp'][0])
                self.node_1_end_time = int(df['time_stamp'][len(df)-1])
            else:
                self.node_2_df = df
                node_2_start_time = int(df['time_stamp'][0])
                node_2_end_time = int(df['time_stamp'][len(df)-1])

                # Matching time
                if self.node_1_start_time > node_2_start_time:
                    print('rake')
                    if self.node_1_end_time < node_2_end_time:
                        self.node_2_df = df.loc[(df['time_stamp'] >= self.node_1_start_time) & (df['time_stamp'] <=
                                                                                                self.node_1_end_time)]
                    else:
                        self.node_2_df = df.loc[(df['time_stamp'] >= self.node_1_start_time)]
                        self.node_1_df = self.node_1_df.loc[(self.node_1_df['time_stamp'] <= node_2_end_time)]
                else:
                    print('roofie')
                    if self.node_1_end_time < node_2_end_time:
                        print('cc')
                        self.node_1_df = self.node_1_df.loc[(self.node_1_df['time_stamp'] >= node_2_start_time)]
                        self.node_2_df = df.loc[(df['time_stamp'] <= self.node_1_end_time)]
                    else:
                        print('pp')
                        self.node_1_df = self.node_1_df.loc[(df['time_stamp'] >= node_2_start_time) &
                                                            (self.node_1_df['time_stamp'] <= node_2_end_time)]

    def test(self):
        self.format_data()
        return self.node_1_df, self.node_2_df


if __name__ == '__main__':
    file_n_s = ['/home/rmr327/Downloads/one.csv', '/home/rmr327/Downloads/second.csv']
    key_gen = KeyGen(file_n_s)
    plt.subplot(211)
    node_1_df_1, node_2_df = key_gen.test()
    file_n_s = ['/home/rmr327/Downloads/one.csv', '/home/rmr327/Downloads/three.csv']
    key_gen = KeyGen(file_n_s)
    node_1_df, node_3_df = key_gen.test()

    # subcarriers = list(range(1, 53))
    # node_1_df_1 = node_1_df_1.groupby('time_stamp')[subcarriers].mean()
    # node_2_df = node_2_df.groupby('time_stamp')[subcarriers].mean()
    # node_3_df = node_3_df.groupby('time_stamp')[subcarriers].mean()
    # print(gk.head())

    node_1_df_1.reset_index(inplace=True, drop=True)
    node_2_df.reset_index(inplace=True, drop=True)
    node_3_df.reset_index(inplace=True, drop=True)

    print(node_1_df_1.columns.values)

    trend = []
    trend_2 = []
    trend_3 = []
    length_1 = len(node_1_df_1)
    length_2 = len(node_2_df)
    length_3 = len(node_3_df)

    pre_trend = []
    pre_2_trend = []
    pre_3_trend = []

    for i in range(length_1):
        temp = 0
        for j in range(15, 30):
            if node_1_df_1[j][i] > node_1_df_1[j-1][i]:
                temp += 1
        pre_trend.append(temp)

    trend_mean = np.mean(pre_trend)
    for i in pre_trend:
        if i > trend_mean:
            trend.append(1)
        else:
            trend.append(0)

    for i in range(length_2):
        temp = 0
        for j in range(15, 30):
            if node_2_df[j][i] > node_2_df[j-1][i]:
                temp += 1
        pre_2_trend.append(temp)

    trend_2_mean = np.mean(pre_2_trend)
    for i in pre_2_trend:
        if i > trend_2_mean:
            trend_2.append(1)
        else:
            trend_2.append(0)

    for i in range(length_3):
        temp = 0
        for j in range(15, 30):
            if node_3_df[j][i] > node_3_df[j-1][i]:
                temp += 1
        pre_3_trend.append(1)

    trend_3_mean = np.mean(pre_3_trend)
    for i in pre_3_trend:
        if i > trend_3_mean:
            trend_3.append(1)
        else:
            trend_3.append(0)

    # print(trend)
    # print(list((trend-np.min(trend)) / (max(trend) - min(trend))))
    # print('rakken')
    # print(trend_2)
    # print(list((trend_2 - np.min(trend_2)) / (max(trend_2) - min(trend_2))))
    # print('shobuj')
    # print(trend_3)
    # print(list((trend_3 - np.min(trend_3)) / (max(trend_3) - min(trend_3))))

    slider = 10
    t_window = 4
    print(pre_trend)
    print(np.mean(pre_trend))
    print(np.mean(pre_2_trend))
    print(np.mean(pre_3_trend))
    trend_w = []
    for w in range(int(len(trend)/slider)):
        num_one = trend[slider * w:slider + (slider * w)].count(1)
        num_zero = trend[slider * w:slider + (slider * w)].count(0)
        if num_one == t_window and num_zero == 10 - t_window:
            trend_w.append(1)
        else:
            trend_w.append(0)
    trend_2_w = []
    for w in range(int(len(trend_2) / slider)):
        num_one = trend_2[slider * w:slider + (slider * w)].count(1)
        num_zero = trend[slider * w:slider + (slider * w)].count(0)
        if num_one == t_window and num_zero == 10 - t_window:
            trend_2_w.append(1)
        else:
            trend_2_w.append(0)

    trend_3_w = []
    for w in range(int(len(trend_3) / slider)):
        num_one = trend_3_w[slider * w:slider + (slider * w)].count(1)
        num_zero = trend[slider * w:slider + (slider * w)].count(0)
        if num_one == t_window and num_zero == 10 - t_window:
            trend_3_w.append(1)
        else:
            trend_3_w.append(0)

    print("DATA1")
    print(trend_w)
    print("DATA2")
    print(trend_2_w)
    print("DATA3")
    print(trend_3_w)
    print(len(trend))
    print(len(trend_w))

    # node_1_df_1 = node_1_df_1.loc[(node_1_df_1[26] > 0.5)]
    # node_2_df = node_2_df.loc[(node_2_df[26] > 0.5)]
    plt.plot(list(range(len(node_1_df_1.columns) - 5)), abs(node_1_df_1.iloc[200, 2: 53]))
    plt.plot(list(range(len(node_2_df.columns) - 5)), abs(node_2_df.iloc[200, 2: 53]), 'r')
    plt.subplot(212)
    # self.node_2_df = self.node_2_df.loc[(self.node_2_df[26] > 0.5)]
    # self.node_2_df = self.node_2_df.loc[(self.node_2_df[26] < 0.7)]
    plt.plot(node_1_df['time_stamp'], node_1_df[26])
    plt.plot(node_3_df['time_stamp'], node_3_df[26], 'g')
    plt.show()
