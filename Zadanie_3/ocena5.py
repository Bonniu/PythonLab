import os
import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import seaborn as sns

dane_2 = pd.read_csv(".\\iris.data", names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class'])
ilosc_danych: int = len(dane_2)


# heatmap
plt.figure(figsize=[10,10])
plt.rcParams.update({'font.size': 15})
_ = sns.heatmap(dane_2.corr(), annot=True, vmin=-1.0, vmax=1.0)



# wykres korelacji
pd.plotting.scatter_matrix(dane_2, figsize=[8, 8])
plt.rcParams.update({'font.size': 15})
plt.show()



# przypisujemy dane do odpowiednich zmiennych
x = dane_2['petal_width'].values.reshape(-1, 1)
y = dane_2['petal_length']

# Dzielimy dane - 50% danych jako zbiór testowy, 250% jak zbiór treningowy
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.50)

regressor = LinearRegression()
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)

# rysowanie wykresu
plt.figure(figsize=[10,10])
plt.rcParams.update({'font.size': 15})
plt.scatter(x_test, y_test,  color='red')
plt.plot(x_test, y_pred, color='violet', linewidth=4)
plt.gca().set(title='Krzywa regresji cech ilościowych (petal_length i petal_width)', 
              ylabel='petal_length', 
              xlabel='petal_width')

plt.show()

