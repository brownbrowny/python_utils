import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timedelta

# Pfade zu den CSV-Dateien eingeben
csv_file_path_1 = input("Bitte den vollständigen Pfad zur ersten CSV-Datei eingeben: ")
csv_file_path_2 = input("Bitte den vollständigen Pfad zur zweiten CSV-Datei eingeben: ")

# Lesen der ersten CSV-Datei
data1 = pd.read_csv(csv_file_path_1, skiprows=1, header=None, names=['Zeitwert', 'Schritte', 'Belohnung'])

# Sicherstellen, dass die Datentypen korrekt sind
data1['Zeitwert'] = data1['Zeitwert'].astype(float)
data1['Schritte'] = data1['Schritte'].astype(int)
data1['Belohnung'] = data1['Belohnung'].astype(float)

# Extrahieren der Spalten
zeitwert1 = data1['Zeitwert']
schritte1 = data1['Schritte']
belohnung1 = data1['Belohnung'] / 100

# Wall time in datetime-Objekte konvertieren
zeitwert_datetime1 = [datetime.fromtimestamp(ts) for ts in zeitwert1]

# Berechnung der vergangenen Zeit seit Beginn des Trainings
start_time1 = zeitwert_datetime1[0]
elapsed_time1 = [(ts - start_time1) for ts in zeitwert_datetime1]

# Lesen der zweiten CSV-Datei
data2 = pd.read_csv(csv_file_path_2, skiprows=1, header=None, names=['Zeitwert', 'Schritte', 'Belohnung'])

# Sicherstellen, dass die Datentypen korrekt sind
data2['Zeitwert'] = data2['Zeitwert'].astype(float)
data2['Schritte'] = data2['Schritte'].astype(int)
data2['Belohnung'] = data2['Belohnung'].astype(float)

# Extrahieren der Spalten
zeitwert2 = data2['Zeitwert']
schritte2 = data2['Schritte']
belohnung2 = data2['Belohnung'] / 100

# Wall time in datetime-Objekte konvertieren
zeitwert_datetime2 = [datetime.fromtimestamp(ts) for ts in zeitwert2]

# Berechnung der vergangenen Zeit seit Beginn des Trainings
start_time2 = zeitwert_datetime2[0]
elapsed_time2 = [(ts - start_time2) for ts in zeitwert_datetime2]

# Schriftart zu Latin Modern ändern
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif'],
    'mathtext.fontset': 'dejavuserif'
})

# Erstellen des Plots
fig, ax1 = plt.subplots(figsize=(20, 10))

# Plotten der Belohnung über die Schritte
ax1.plot(schritte1, belohnung1, color='blue', label='Training 1')
ax1.plot(schritte2, belohnung2, color='green', label='Training 2')
ax1.set_xlabel('Schritte x$10^5$', fontsize=18, labelpad=20)
ax1.set_ylabel('Belohnung', fontsize=20, labelpad=20)
ax1.legend(fontsize=20)
ax1.tick_params(axis='both', which='major', labelsize=16)
ax1.grid(True)

# x-Achse Ticks alle 200.000 Schritte
ax1.set_xticks(np.arange(0, max(schritte1.max(), schritte2.max()) + 1, 2*10**5))

# Funktion zum Formatieren der Ticks
def format_func(value, tick_number):
    return f'{int(value / 10**5)}'

# Anwenden des Formatters auf die x-Achse
ax1.xaxis.set_major_formatter(FuncFormatter(format_func))

# x-Tick-Labels vertikal ausrichten
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)

# Sekundäre x-Achse für Zeitwert
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())

# Bestimmen, welche Datei weiter in die Zukunft reicht
if zeitwert_datetime1[-1] > zeitwert_datetime2[-1]:
    zeitwert_datetime = zeitwert_datetime1
    elapsed_time = elapsed_time1
    schritte = schritte1
else:
    zeitwert_datetime = zeitwert_datetime2
    elapsed_time = elapsed_time2
    schritte = schritte2

# Berechnung der vergangenen Zeit in Minuten und Stunden
elapsed_minutes = [et.total_seconds() // 60 for et in elapsed_time]
elapsed_hours_minutes = [(int(elapsed // 60), int(elapsed % 60)) for elapsed in elapsed_minutes]

# Setzen der Ticks in Intervallen von 5 Minuten
max_time = int(elapsed_minutes[-1])
tick_positions = np.arange(0, max_time + 5, 5)
tick_labels = [f'{hours}h {minutes}min' for hours, minutes in [(tick // 60, tick % 60) for tick in tick_positions]]

# Anwenden der Ticks und Labels auf die sekundäre x-Achse
ax2.set_xticks(tick_positions * (max(schritte) / max_time))
ax2.set_xticklabels(tick_labels)
ax2.set_xlabel('Vergangene Zeit', fontsize=18, labelpad=20)
ax2.tick_params(axis='both', which='major', labelsize=16)

# x-Tick-Labels vertikal ausrichten
for tick in ax2.get_xticklabels():
    tick.set_rotation(45)

# Anzeigen des Plots
plt.tight_layout()
plt.show()
