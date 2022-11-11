import numpy as np
from sklearn.preprocessing import PolynomialFeatures
import pickle

FINALIZED_MODEL = "finalized_model.sav"

# Load the trained model
loaded_model = pickle.load(open(FINALIZED_MODEL, 'rb'))

# Predict Daily New Cases using the machine learning model
positivityRate = np.array(0.02).reshape(-1, 1)

polyFeature = PolynomialFeatures(degree=5)
x_predict = polyFeature.fit_transform(positivityRate)
predicted_y = loaded_model.predict(x_predict)
print(predicted_y[0][0])
