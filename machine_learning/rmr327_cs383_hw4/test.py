import pandas as pd
import numpy as np
from math import exp, pow, pi, sqrt
from scipy import stats


class NaiveBayesClassifier:
    def __init__(self, file_name):
        self.file_name = file_name
        self.testing_target_data = None
        self.testing_feature_data = None
        self.training_f_d_spam = None
        self.training_f_d_not_spam = None
        self.total_training_observations = None
        self.prior_data_spam = None
        self.prior_data_not_spam = None
        self.mean_spam_data = None
        self.mean_not_spam_data = None
        self.std_spam_data = None
        self.std_not_spam_data = None

    def pre_process_data(self):
        data = pd.read_csv(self.file_name, header=None)  # Reading in data
        data = data.sample(frac=1, random_state=0).reset_index(drop=True)  # Lets randomize our data with seed 0

        # Splitting testing and training data
        len_data = len(data)
        data_divider = int(np.ceil((2 / 3) * len_data))  # 2/3 marker for splitting the data)
        training_data = data.iloc[: data_divider]
        testing_data = data.iloc[data_divider:]
        testing_data = pd.DataFrame(testing_data.reset_index(drop=True))

        # Splitting on target and features
        training_target_data = training_data.iloc[:, -1]
        self.testing_target_data = testing_data.iloc[:, -1]
        training_feature_data = training_data.iloc[:, :-1]
        self.testing_feature_data = testing_data.iloc[:, :-1]

        # Lets keep a tab on how many training observations we have
        self.total_training_observations = len(training_target_data)

        # Standardizing using the training data
        training_feature_data = (training_feature_data - training_feature_data.mean()) / training_feature_data.std(
            ddof=1)

        # Lets put back out training data
        training_data = pd.concat([training_feature_data, training_target_data], axis=1)

        # Lets divide into spam and not spam groups
        self.training_f_d_spam = training_data.loc[(training_data.iloc[:, -1] == 1)]
        self.training_f_d_not_spam = training_data.loc[(training_data.iloc[:, -1] != 1)]

    def create_normal_model(self):
        self.pre_process_data()

        # Lets Find priors of spam and not spam
        self.prior_data_spam = len(self.training_f_d_spam) / self.total_training_observations
        self.prior_data_not_spam = len(self.training_f_d_not_spam) / self.total_training_observations

        # Lets find out gaussian parameters
        self.mean_spam_data = self.training_f_d_spam.iloc[:, 0:-1].mean()
        self.mean_not_spam_data = self.training_f_d_not_spam.iloc[:, 0:-1].mean()
        self.std_spam_data = self.training_f_d_spam.iloc[:, 0:-1].var()
        self.std_not_spam_data = self.training_f_d_not_spam.iloc[:, 0:-1].var()

    @staticmethod
    def get_prob(data_points, mean, std):
        output = []
        for data_point in data_points:
            res = 1 / (np.sqrt(2 * np.pi * std)) * np.exp((-(data_point - mean) ** 2) / (2 * std))
            output.append(res)

        return output

    def classify(self):
        self.create_normal_model()
        # Standardizing using the testing data
        testing_feature_data = (self.testing_feature_data -
                                self.testing_feature_data.mean()) / self.testing_feature_data.std(ddof=1)

        # Adding a predicted column for the test data
        self.testing_target_data = pd.DataFrame(self.testing_target_data)
        self.testing_target_data['predicted'] = None

        # Finding PDF
        prob_spam = testing_feature_data.apply(lambda x: self.get_prob(x.values, self.mean_spam_data.iloc[
            int(x.name)], self.std_spam_data.iloc[int(x.name)]))
        print(prob_spam)
        prob_spam = stats.norm.pdf(testing_feature_data, self.mean_spam_data, self.std_spam_data)
        prob_not_spam = stats.norm.pdf(testing_feature_data, self.mean_not_spam_data, self.std_not_spam_data)
        # print(pd.DataFrame(prob_spam).head())

        # Finding maximum likelihood estimate
        mle_spam = np.prod(prob_spam, axis=1)
        mle_not_spam = np.prod(prob_not_spam, axis=1)

        # Finding estimated probability of test samples for both spam and not spam
        p_est_spam__ytest = (self.prior_data_spam * mle_spam)
        p_est_not_spam_ytest = (self.prior_data_not_spam * mle_not_spam)

        # Lets get out predictions
        # for i in range(len(p_est_spam__ytest)):
        #     print(p_est_spam__ytest[i], p_est_not_spam_ytest[i], self.testing_target_data.iloc[i, 0])

        # for j in range(len(testing_feature_data)):
        #     probability_spam = self.prior_data_spam
        #     probability_not_spam = self.prior_data_not_spam
        #     for i in range(len(self.testing_feature_data.columns)):
        #         p_x_given_spam = (1/sqrt(2*3.14*self.std_spam_data[j][i])) * \
        #                          exp(-0.5 * pow((testing_feature_data[i] - self.mean_spam_data[j][i]), 2
        #                                         )/self.std_spam_data[j][i])

        #         p_x_given_not_spam = (1 / (self.std_not_spam_data.iloc[i] * np.sqrt(2 * np.pi))) * exp(
        #             -((testing_feature_data.iloc[j, i] - self.mean_not_spam_data.iloc[i]) ** 2) / (
        #                         2 * (self.std_not_spam_data.iloc[i] ** 2)))

        #         if p_x_given_spam > 1:
        #             # print(self.std_spam_data.iloc[i], testing_feature_data.iloc[j, i], self.mean_spam_data.iloc[i], p_x_given_spam)
        #         probability_spam = probability_spam * p_x_given_spam
        #         probability_not_spam = probability_not_spam * p_x_given_not_spam

        #     normalized_prob_spam = probability_spam / (probability_not_spam + probability_spam)
        #     normalized_prob_not_spam = probability_not_spam / (probability_not_spam + probability_spam)

        #     if normalized_prob_spam > normalized_prob_not_spam:
        #         self.testing_target_data.iloc[j, -1] = 1
        #     else:
        #         self.testing_target_data.iloc[j, -1] = 0

        # print(self.testing_target_data)


if __name__ == '__main__':
    naive_bayes_classifier = NaiveBayesClassifier('spambase.data')
    naive_bayes_classifier.classify()
