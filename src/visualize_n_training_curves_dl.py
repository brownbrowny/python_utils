import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timedelta

# Anzahl der CSV-Dateien eingeben
n = int(input("Bitte die Anzahl der CSV-Dateien eingeben: "))

# Listen zum Speichern der Daten und Legendenwerte
all_schritte = []
all_Verlust = []
all_zeitwert_datetime = []
all_elapsed_time = []
legends = []
max_elapsed_time = timedelta(0)

# CSV-Dateien einlesen
for i in range(n):
    csv_file_path = input(f"Bitte den vollständigen Pfad zur CSV-Datei {i+1} eingeben: ")
    legend = input(f"Bitte den Legendenwert für Kurve {i+1} eingeben: ")
    legends.append(legend)
    
    # Lesen der CSV-Datei
    data = pd.read_csv(csv_file_path, skiprows=1, header=None, names=['Zeitwert', 'Schritte', 'Verlust'])
    
    # Sicherstellen, dass die Datentypen korrekt sind
    data['Zeitwert'] = data['Zeitwert'].astype(float)
    data['Schritte'] = data['Schritte'].astype(int)
    data['Verlust'] = data['Verlust'].astype(float) / 100
    
    # Extrahieren der Spalten
    zeitwert = data['Zeitwert']
    schritte = data['Schritte']
    Verlust = data['Verlust']
    
    # Wall time in datetime-Objekte konvertieren
    zeitwert_datetime = [datetime.fromtimestamp(ts) for ts in zeitwert]
    
    # Berechnung der vergangenen Zeit seit Beginn des Trainings
    start_time = zeitwert_datetime[0]
    elapsed_time = [(ts - start_time) for ts in zeitwert_datetime]
    
    # Speichern der Daten
    all_schritte.append(schritte)
    all_Verlust.append(Verlust)
    all_zeitwert_datetime.append(zeitwert_datetime)
    all_elapsed_time.append(elapsed_time)
    
    # Bestimmen der maximalen Zeit
    if elapsed_time[-1] > max_elapsed_time:
        max_elapsed_time = elapsed_time[-1]
        max_elapsed_schritte = schritte
        max_elapsed_minutes = [et.total_seconds() // 60 for et in elapsed_time]
        max_elapsed_hours_minutes = [(int(elapsed // 60), int(elapsed % 60)) for elapsed in max_elapsed_minutes]

# Schriftart zu Latin Modern ändern
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif'],
    'mathtext.fontset': 'dejavuserif'
})

# Farben definieren
colors = ['blue', 'red', 'green'] + [None] * (n - 3)

# Erstellen des Plots
fig, ax1 = plt.subplots(figsize=(20, 10))

# Plotten der Verlust über die Schritte
for i in range(n):
    color = colors[i] if i < len(colors) else None
    ax1.plot(all_schritte[i], all_Verlust[i], color=color, label=legends[i])
ax1.set_xlabel('Episoden', fontsize=18, labelpad=20)
ax1.set_ylabel('Verlust', fontsize=20, labelpad=20)
ax1.legend(fontsize=20)
ax1.tick_params(axis='both', which='major', labelsize=16)
ax1.grid(True)

# x-Achse Ticks alle 200.000 Schritte
ax1.set_xticks(np.arange(0, max(max(all_schritte, key=lambda x: x.max())) + 1, 50))

# Funktion zum Formatieren der Ticks
def format_func(value, tick_number):
    return f'{int(value / 10**6)}'

# Anwenden des Formatters auf die x-Achse
# ax1.xaxis.set_major_formatter(FuncFormatter(format_func))

# x-Tick-Labels vertikal ausrichten
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)

# Sekundäre x-Achse für Zeitwert
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())

# Setzen der Ticks in n Zeit-Intervallen
tick_interval = 240  # 12 Stunden in Minuten
max_time = int(max_elapsed_minutes[-1])
tick_positions = np.arange(0, max_time + tick_interval, tick_interval)

# Dynamisches Erstellen der Tick-Labels
tick_labels = []
for tick in tick_positions:
    days, remainder = divmod(tick, 1440)  # 1440 Minuten in einem Tag
    hours, minutes = divmod(remainder, 60)
    if max_time >= 1440:  # Wenn die Zeitdauer länger als ein Tag ist
        tick_labels.append(f'{days}d {hours}h')
    else:
        tick_labels.append(f'{hours}h {minutes}min')

# Anwenden der Ticks und Labels auf die sekundäre x-Achse
ax2.set_xticks(tick_positions * (max(max_elapsed_schritte) / max_time))
ax2.set_xticklabels(tick_labels)
ax2.set_xlabel('Vergangene Zeit', fontsize=18, labelpad=20)
ax2.tick_params(axis='both', which='major', labelsize=16)

# x-Tick-Labels vertikal ausrichten
for tick in ax2.get_xticklabels():
    tick.set_rotation(45)

# Anzeigen des Plots
plt.tight_layout()
plt.show()
