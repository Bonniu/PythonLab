import os
import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dane_2 = pd.read_csv("iris.data", names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class'])
ilosc_danych: int = len(dane_2)
print(dane_2)
#
# -----------------------------------------Wymagania na ocenę dobrą
#
# Wyznaczyć macierz korelacji dla cech ilościowych.
# Narysować histogramy dla dwóch cech ilościowych najbardziej ze sobą skorelowanych.
# Zadbać o czytelność rezultatów oraz staranny i atrakcyjny wygląd histogramów.


# macierz korelacji
# Wartość współczynnika korelacji mieści się w przedziale domkniętym [-1, 1].
# Im większa jego wartość bezwzględna, tym silniejsza jest zależność liniowa między zmiennymi.
#  r_{xy}=0 oznacza brak liniowej zależności między cechami,
#  r_{xy}=1 oznacza dokładną dodatnią liniową zależność między cechami, natomiast
#  r_{xy}=-1 oznacza dokładną ujemną liniową zależność między cechami,
#  tzn. jeżeli zmienna x rośnie, to y maleje i na odwrót.


print(dane_2.corr())
#  w macierzy widać że najbardziej są skorelowane ze sobą sąpetal_length i petal_width (0.962757)

plt.figure(figsize=[10,10])
plt.rcParams.update({'font.size': 15})
plt.hist(dane_2.petal_length, bins=22, range=(0, 10), color='#FF0000')
plt.gca().set(title='petal_length - histogram', ylabel='Częstość', xlabel='petal_length')
plt.show()



plt.figure(figsize=[10,10])
plt.rcParams.update({'font.size': 15})
plt.hist(dane_2.petal_width, bins=13, range=(0, 3), color='#00FF00')
plt.gca().set(title='petal_width - histogram', ylabel='Częstość', xlabel='petal_width')
plt.show()
