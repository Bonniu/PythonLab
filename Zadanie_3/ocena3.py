import pandas as pd
import numpy as np
import matplotlib as plt
import os
import statistics

print(os.getcwd())

# dane = pd.read_csv("../fertility_diagnosis.data")
dane = pd.read_csv(".\\fertility_Diagnosis.data")
ilosc_danych: int = len(dane)

# w przypadku cech ilościowych: średnią arytmetyczną, odchylenie
# standardowe, medianę, minimum i maksimum;
# w przypadku cech jakościowych: dominantę, wskazując jednocześnie jej liczebność i częstość.


print("\nCecha ilościowa: Season")
print("""Opis: Sezon, w którym przeprowadzono analizę. 
         1) zima, 
         2) wiosna, 
         3) lato, 
         4) jesień. 
         (-1, -0,33, 0,33, 1)""")
season = dane.Season
dominant = statistics.mode(season)
licznik = len([1 for i in season if i == dominant])
print("Dominanta: ", dominant)
print("Liczebność: ", licznik)
print("Częstość: ", licznik / ilosc_danych)

print("\nCecha ilościowa: Age")
print("Opis: Wiek w momencie analizy. 18–36 (0, 1)")
age = round(dane.Age * 18) + 18
print("Średnia: ", statistics.mean(age))
print("Odchylenie standardowe: ", statistics.stdev(age))
print("Mediana: ", statistics.median(age))
print("Maksimum: ", max(age))
print("Minimum: ", min(age))

print("\nCecha jakościowa: IfDiseases")
print("Opis: Choroby dziecięce (tj. Ospa wietrzna, odra, świnka, polio) 1) tak, 2) nie. (0, 1)")
if_diseases = dane.IfDiseases
dominant = statistics.mode(if_diseases)
licznik = len([1 for i in if_diseases if i == dominant])
print("Dominanta: ", dominant)
print("Liczebność: ", licznik)
print("Częstość: ", licznik / ilosc_danych)

print("\nCecha jakościowa: IfTrauma")
print("Wypadek lub poważna trauma 1) tak, 2) nie. (0, 1)")
if_trauma = dane.IfTrauma
dominant = statistics.mode(if_trauma)
licznik = len([1 for i in if_trauma if i == dominant])
print("Dominanta: ", dominant)
print("Liczebność: ", licznik)
print("Częstość: ", licznik / ilosc_danych)

print("\nCecha jakościowa: IfIntervention")
print("Opis: Interwencja chirurgiczna 1) tak, 2) nie. (0, 1)")
if_intervention = dane.IfIntervention
dominant = statistics.mode(if_intervention)
licznik = len([1 for i in if_intervention if i == dominant])
print("Dominanta: ", dominant)
print("Liczebność: ", licznik)
print("Częstość: ", licznik / ilosc_danych)

print("\nCecha jakościowa: IfFever")
print("""Opis: Wysokie gorączki w ostatnim roku 
        1) mniej niż trzy miesiące temu, 
        2) więcej niż trzy miesiące temu, 
        3) nie. 
        (-1, 0, 1)""")
if_fever = dane.IfFever
dominant = statistics.mode(if_fever)
licznik = len([1 for i in if_fever if i == dominant])
print("Dominanta: ", dominant)
print("Liczebność: ", licznik)
print("Częstość: ", licznik / ilosc_danych)

print("\nCecha jakościowa: FreqOfAlc")
print("""Częstotliwość spożywania alkoholu 
            1) kilka razy dziennie, 
            2) każdego dnia, 
            3) kilka razy w tygodniu, 
            4) raz w tygodniu, 
            5) prawie nigdy lub nigdy 
            (0, 1)
""")
freq_of_alc = dane.FreqOfAlc
dominant = statistics.mode(freq_of_alc)
licznik = len([1 for i in freq_of_alc if i == dominant])
print("Dominanta: ", dominant)
print("Liczebność: ", licznik)
print("Częstość: ", licznik / ilosc_danych)

print("\nCecha jakościowa: SmokingHabit")
print("""Nałóg palenia 
            1) nigdy, 
            2) okazjonalnie 
            3) codziennie. 
            (-1, 0, 1)""")
smoking_habit = dane.SmokingHabit
dominant = statistics.mode(smoking_habit)
licznik = len([1 for i in smoking_habit if i == dominant])
print("Dominanta: ", dominant)
print("Liczebność: ", licznik)
print("Częstość: ", licznik / ilosc_danych)

print("\nCecha jakościowa: SitHours")
print("""Liczba godzin spędzonych na siedzeniu dziennie ene-16 (0, 1)""")
sit_hours = dane.SitHours
dominant = statistics.mode(smoking_habit)
licznik = len([1 for i in smoking_habit if i == dominant])
print("Dominanta: ", dominant)
print("Liczebność: ", licznik)
print("Częstość: ", licznik / ilosc_danych)

print("\nCecha jakościowa: Output")
print("""Wyjście: diagnoza normalna (N), zmieniona (O)""")
output = dane.Output
dominant = statistics.mode(output)
licznik = len([1 for i in output if i == dominant])
print("Dominanta: ", dominant)
print("Liczebność: ", licznik)
print("Częstość: ", licznik / ilosc_danych)





