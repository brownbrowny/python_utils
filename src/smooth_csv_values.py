import pandas as pd
import numpy as np

# Funktion zur Glättung der Werte
def smooth(values, weight):
    last = values[0]
    smoothed = []
    for value in values:
        smoothed_val = last * weight + (1 - weight) * value
        smoothed.append(smoothed_val)
        last = smoothed_val
    return smoothed

# Pfad zur Eingabedatei abfragen
input_file = input("Geben Sie den Pfad zur CSV-Datei ein: ")
output_file = input_file.replace('.csv', '_smoothed.csv')

# CSV-Datei einlesen
df = pd.read_csv(input_file)

# Glättung durchführen
weight = float(input("Geben Sie den Glättungsfaktor ein (zwischen 0 und 1): "))
df['Value'] = smooth(df['Value'], weight)

# Neue CSV-Datei mit geglätteten Werten speichern
df.to_csv(output_file, index=False)

print(f"Die geglättete Datei wurde unter {output_file} gespeichert.")
