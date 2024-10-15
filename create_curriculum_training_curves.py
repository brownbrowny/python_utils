import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timedelta

# Anzahl der CSV-Dateien
n = 8

# Pfade zu den CSV-Dateien und Legendenwerte
csv_file_paths = [
    r"C:\Users\wn00194953\Downloads\angle_0_smoothed.csv",
    r"C:\Users\wn00194953\Downloads\angle_2_smoothed.csv",
    r"C:\Users\wn00194953\Downloads\angle_4_smoothed.csv",
    r"C:\Users\wn00194953\Downloads\angle_6_1_smoothed.csv",
    r"C:\Users\wn00194953\Downloads\angle_8_1_smoothed.csv",
    r"C:\Users\wn00194953\Downloads\angle_10_1_smoothed.csv",
    r"C:\Users\wn00194953\Downloads\angle_12_1_smoothed.csv",
    r"C:\Users\wn00194953\Downloads\angle_14_1_smoothed.csv"
]

legends = [
    "0 Grad", "2 Grad", "4 Grad", "6 Grad",
    "8 Grad", "10 Grad", "12 Grad", "14 Grad"
]

# Listen zum Speichern der Daten
all_schritte = []
all_belohnung = []
all_zeitwert_datetime = []
all_elapsed_time = []
max_elapsed_time = timedelta(0)

# CSV-Dateien einlesen
for i in range(n):
    csv_file_path = csv_file_paths[i]
    
    # Lesen der CSV-Datei
    data = pd.read_csv(csv_file_path, skiprows=1, header=None, names=['Zeitwert', 'Schritte', 'Belohnung'])
    
    # Sicherstellen, dass die Datentypen korrekt sind
    data['Zeitwert'] = data['Zeitwert'].astype(float)
    data['Schritte'] = data['Schritte'].astype(int)
    data['Belohnung'] = data['Belohnung'].astype(float)
    
    # Extrahieren der Spalten
    zeitwert = data['Zeitwert']
    schritte = data['Schritte']
    belohnung = data['Belohnung'] / 100
    
    # Wall time in datetime-Objekte konvertieren
    zeitwert_datetime = [datetime.fromtimestamp(ts) for ts in zeitwert]
    
    # Berechnung der vergangenen Zeit seit Beginn des Trainings
    start_time = zeitwert_datetime[0]
    elapsed_time = [(ts - start_time) for ts in zeitwert_datetime]
    
    # Speichern der Daten
    all_schritte.append(schritte)
    all_belohnung.append(belohnung)
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

# Plotten der Belohnung über die Schritte
for i in range(n):
    color = colors[i] if i < len(colors) else None
    ax1.plot(all_schritte[i], all_belohnung[i], color=color, label=legends[i])
ax1.set_xlabel('Schritte x$10^6$', fontsize=28, labelpad=20)
ax1.set_ylabel('Belohnung', fontsize=28, labelpad=20)
ax1.legend(fontsize=28)
ax1.minorticks_on()
ax1.tick_params(axis='both', which='major', labelsize=26, width=2, length=4)
ax1.grid(True)

# x-Achse Ticks alle 1.000.000 Schritte
ax1.set_xticks(np.arange(0, max(max(all_schritte, key=lambda x: x.max())) + 1, 2*10**6))

# Funktion zum Formatieren der Ticks
def format_func(value, tick_number):
    return f'{int(value / 10**6)}'

# Anwenden des Formatters auf die x-Achse
ax1.xaxis.set_major_formatter(FuncFormatter(format_func))

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
ax2.set_xlabel('Vergangene Zeit', fontsize=28, labelpad=20)
ax2.minorticks_on()
ax2.tick_params(axis='both', which='major', labelsize=26, width=2, length=4)

# Anzeigen des Plots
plt.tight_layout()
plt.show()
