import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

df= pd.read_csv('flu_factors.csv')
Y = df["Infected"]
X = df.drop("Infected", axis = 1).drop("Name", axis = 1)

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,train_size = 0.90, random_state = 1)

lr = LinearRegression()
lr.fit(X_train,Y_train)

print(X_train[:10])
data_new = X_train[:10]
print(lr.predict(data_new))
print(Y_train[:10])

age = int(input("Age: "))
obese = int(input("Obese: "))
vax = int(input("Vax: "))
sun = int(input("sun: "))
sup = int(input("sup: "))
sleep = int(input("sleep: "))
anti = int(input("anti: "))
dia = int(input("dia: "))
heart = int(input("heart: "))

over65=0
under5=0
if (age<5):
    under5=1
if(age>65):
    over65=1

predict = X_train[:1].copy()
predict.iloc[[0],[0]] = age
predict.iloc[[0],[1]] = over65
predict.iloc[[0],[2]] = under5
predict.iloc[[0],[4]] = obese
predict.iloc[[0],[5]] = vax
predict.iloc[[0],[6]] = sun
predict.iloc[[0],[7]] = sup
predict.iloc[[0],[8]] = sleep
predict.iloc[[0],[9]] = anti
predict.iloc[[0],[10]] = dia
predict.iloc[[0],[11]] = heart

print(predict)

print(lr.predict(predict))


