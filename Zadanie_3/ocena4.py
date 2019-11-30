import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import statistics

dane = pd.read_csv(".\\iris.data")
ilosc_danych: int = len(dane)
print(dane)
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


print(dane.corr())
#  w macierzy widać że najbardziej są skorelowane ze sobą sąpetal_length i petal_width (0.962757)

#  wykresy
plt.hist(dane.petal_length, bins=22, range=(0, 10), color='#FF0000')
plt.show()

plt.hist(dane.petal_width, bins=13, range=(0, 3), color='#00FF00')
plt.show()

# pozdro 5 linii na ocene 4 XD
