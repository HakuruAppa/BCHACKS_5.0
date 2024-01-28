import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.linear_model import LogisticRegression

df= pd.read_csv('flu_factors.csv')
y = df["Infected"]
X = df.drop("Infected", axis = 1).drop("Name", axis = 1)

X_train,X_test,y_train,y_test=train_test_split(
    X,y, 
    train_size = 0.80, 
    random_state = 1)

lr = LinearRegression()
lr.fit(X_train,y_train)

data_new = X_train[:4]
print(lr.predict(data_new))
print(y_train[:4])
