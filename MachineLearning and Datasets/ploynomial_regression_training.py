import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import pickle

# Load data
data = pd.read_csv('covid19_clean.csv', sep = ',')
data = data[['Daily New Cases', 'Positivity Rate']]


# Labels for graphs
plt.scatter(data['Positivity Rate'], data['Daily New Cases'], label="Original Data")
plt.title("Daily New Cases Per Day based on Positivity Rate")
plt.xlabel("Positivity Rates")
plt.ylabel("Number of Daily New Cases")

# Prepare data
x = np.array(data['Positivity Rate']).reshape(-1, 1)
y = np.array(data['Daily New Cases']).reshape(-1, 1)

# Fitting the input data and create the linear model based on the polynomial data
polyFeat = PolynomialFeatures(degree=5)
x_train_poly = polyFeat.fit_transform(x)
model = linear_model.LinearRegression()
model.fit(x_train_poly, y)
# accuracy = model.score(x_train_poly, y)
# print(round(accuracy*100, 3))

# Save trained model to disk
filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

# Predict Daily New Cases using the machine learning model
predicted_y = model.predict(x_train_poly)

# Outputs graphs
plt.scatter(x, predicted_y, label="Predicted Data")
plt.legend()
plt.show()