from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

data = pd.read_csv('x06Simple.csv').iloc[:, 1:]
data = data.sample(frac=1, random_state=0).reset_index(drop=True)  # Lets randomize our data with seed 0
target_data = data.iloc[:, 0]
feature_data = data.iloc[:, 1:]
feature_data = (feature_data - feature_data.mean())/feature_data.std()  # Standardizing

# Split the dataset into the training set and test set
# We're splitting the data in 1/3, so out of 30 rows, 20 rows will go into the training set,
# and 10 rows will go into the testing set.
xTrain, xTest, yTrain, yTest = train_test_split(feature_data, target_data, test_size=1/5, random_state=0)

linearRegressor = LinearRegression()
linearRegressor.fit(xTrain, yTrain)
yPrediction = linearRegressor.predict(xTest)

rmse = np.sqrt((yTest.sub(yPrediction)).pow(2).sum()/len(yPrediction))

print('RMSE: {}'.format(rmse))
