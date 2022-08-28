import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle


dataset = pd.read_csv('F:/Downloads/Dyscalculia_ComputationalSkills.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

from sklearn.ensemble import RandomForestRegressor
classifier = RandomForestRegressor(n_estimators = 10, random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

classifier.score(X_test, y_test)

model1 = classifier.predict([[1,1,1,1,1,1,1,1,1,0]])
print(model1)
pickle.dump(model1,open('dyscal1.pkl','wb'))



dataset1 = pd.read_csv('F:/Downloads/Dyscalculia_MathFluency.csv')
X1 = dataset1.iloc[:, :-1].values
y1 = dataset1.iloc[:, -1].values
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size = 0.20, random_state = 10)
classifier1 = RandomForestRegressor(n_estimators = 10, random_state = 0)
classifier1.fit(X1_train, y1_train)

y1_pred = classifier1.predict(X1_test)
#print(np.concatenate((y1_pred.reshape(len(y1_pred),1), y1_test.reshape(len(y1_test),1)),1))

classifier1.score(X1_test, y1_test)

model2 = classifier1.predict([[1,1,1,1,1,1,1,1,1,0,1]])
print(model2)
pickle.dump(model2,open('dyscal2.pkl','wb'))



dataset2 = pd.read_csv('F:/Downloads/Dyscalculia_MentalComputation.csv')
X2 = dataset2.iloc[:, :-1].values
y2 = dataset2.iloc[:, -1].values
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size = 0.25, random_state = 10)
classifier2 = RandomForestRegressor(n_estimators = 10, random_state = 0)
classifier2.fit(X2_train, y2_train)

y2_pred = classifier2.predict(X2_test)
#print(np.concatenate((y2_pred.reshape(len(y2_pred),1), y2_test.reshape(len(y2_test),1)),1))

classifier2.score(X2_test, y2_test)

model3 = classifier2.predict([[1,0,0,1,1,1,1,1]])
pickle.dump(model3,open('dyscal3.pkl','wb'))
print(model3)



dataset3 = pd.read_csv('F:/Downloads/Dyscalculia_WordProblems.csv')
X3 = dataset3.iloc[:, :-1].values
y3 = dataset3.iloc[:, -1].values
X3_train, X3_test, y3_train, y3_test = train_test_split(X3, y3, test_size = 0.30, random_state = 5)
classifier3 = RandomForestRegressor(n_estimators = 10, random_state = 0)
classifier3.fit(X3_train, y3_train)

y3_pred = classifier3.predict(X3_test)
#print(np.concatenate((y3_pred.reshape(len(y3_pred),1), y3_test.reshape(len(y3_test),1)),1))

classifier3.score(X3_test, y3_test)
model4 = classifier3.predict([[1,0,0,1,1,1,1,1,1]])
pickle.dump(model4,open('dyscal4.pkl','wb'))
print(float(model4))



dataset_dyscalculia = pd.read_csv('F:/Downloads/Dyscalculia.csv')
X_dyscalculia = dataset_dyscalculia.iloc[:, :-1].values
y_dyscalculia = dataset_dyscalculia.iloc[:, -1].values

X_train_dyscalculia, X_test_dyscalculia, y_train_dyscalculia, y_test_dyscalculia = train_test_split(X_dyscalculia, y_dyscalculia, test_size = 0.30, random_state = 10)

from sklearn.linear_model import LogisticRegression
classifier_dyscalculia = LogisticRegression( random_state =0)
classifier_dyscalculia.fit(X_train_dyscalculia, y_train_dyscalculia)

y_pred_dyscalculia = classifier_dyscalculia.predict(X_test_dyscalculia)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test_dyscalculia, y_pred_dyscalculia)
print(cm)
accuracy_score(y_test_dyscalculia, y_pred_dyscalculia)

x = classifier_dyscalculia.predict_proba([[float(model1),float(model2),float(model3),float(model4)]])
print("Dyscalculia Present Probability: ", round(x[0][1]*100, 2))
print("Dyscalculia Absent Probability: ", round(x[0][0]*100, 2))


pickle.dump(classifier_dyscalculia,open('dyscal_model.pkl','wb'))