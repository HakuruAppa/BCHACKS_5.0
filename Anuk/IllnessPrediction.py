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

data_new = X_train[:10]

userDataFile=open("reg_result.txt", 'r')
userData=userDataFile.readline()
dataSplit=userData.split()

for i in dataSplit:
    print(i)

age = int(dataSplit[0])
obese = int(dataSplit[3])
vax = int(dataSplit[4])
sun = int(dataSplit[5])
sup = int(dataSplit[6])
sleep = int(dataSplit[7])
anti = int(dataSplit[8])
dia = int(dataSplit[9])
heart = int(dataSplit[10])

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

illnessResult=lr.predict(predict)

print(illnessResult)


userDataFile.close()

resultFile = open('illness_result.txt', 'w')
result=illnessResult.astype(str)
resultFile.write(result[0])
resultFile.close()  

