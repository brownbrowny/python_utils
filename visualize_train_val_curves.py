import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Dateipfade eingeben
train_loss_file = input("Pfad zur Datei mit dem Trainingsverlust: ")
val_loss_file = input("Pfad zur Datei mit dem Validierungsverlust: ")

# Daten einlesen
train_loss_df = pd.read_csv(train_loss_file)
val_loss_df = pd.read_csv(val_loss_file)

# Schriftart zu Latin Modern ändern
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif'],
    'mathtext.fontset': 'dejavuserif'
})

# Plot erstellen
fig, ax1 = plt.subplots(figsize=(10, 6))

# Trainingsverlust plotten
ax1.plot(train_loss_df['Step'], train_loss_df['Value'], color='red', label='Trainingsverlust')

# Validierungsverlust plotten
ax1.plot(val_loss_df['Step'], val_loss_df['Value'], color='blue', label='Validierungsverlust')

# Episode abfragen
episode = int(input("Wert für Episode, um einen Punkt zu markieren: "))

# Grünen Kreis um den entsprechenden Punkt in der Validierungskurve zeichnen und beschriften
val_point = val_loss_df[val_loss_df['Step'] == episode]
if not val_point.empty:
    ax1.scatter(val_point['Step'], val_point['Value'], color='lime', edgecolor='lime', facecolor='none', linewidths=2, s=500, label=f'Episode {episode}')

# Achsenbeschriftungen und Legende
ax1.set_xlabel('Episode', fontsize=22)
ax1.set_ylabel('Verlust', fontsize=22)
ax1.legend(fontsize=22)

# Ticks der unteren x-Achse anpassen (volle Hunderterwerte)
max_step = max(train_loss_df['Step'].max(), val_loss_df['Step'].max())
ax1.set_xticks(range(0, max_step + 1, 100))
ax1.tick_params(axis='both', which='major', labelsize=20)

# Sekundäre x-Achse für Zeitwert
ax2 = ax1.twiny()

# Wall time in datetime-Objekte konvertieren und berechnen der Zeit in Sekunden
train_loss_df['Wall time'] = train_loss_df['Wall time'].apply(lambda x: datetime.fromtimestamp(x))
val_loss_df['Wall time'] = val_loss_df['Wall time'].apply(lambda x: datetime.fromtimestamp(x))

# Wandelt Wall time in Sekunden seit Beginn des Trainings um
start_time = min(train_loss_df['Wall time'].min(), val_loss_df['Wall time'].min())
train_loss_df['Elapsed Time'] = (train_loss_df['Wall time'] - start_time).dt.total_seconds()
val_loss_df['Elapsed Time'] = (val_loss_df['Wall time'] - start_time).dt.total_seconds()

# Anpassung der zweiten x-Achse
ax2.set_xlim(ax1.get_xlim())
# Zeit-Ticks alle 8 Stunden
max_time = int(max(train_loss_df['Elapsed Time'].max(), val_loss_df['Elapsed Time'].max()))
tick_positions = range(0, max_time + 1, 8 * 3600)

# Dynamisches Erstellen der Tick-Labels
tick_labels = []
for tick in tick_positions:
    minutes = tick // 60
    days, remainder = divmod(minutes, 1440)  # 1440 Minuten in einem Tag
    hours, minutes = divmod(remainder, 60)
    if max_time >= 1440 * 60:  # Wenn die Zeitdauer länger als ein Tag ist
        tick_labels.append(f'{days}d {hours}h')
    else:
        tick_labels.append(f'{hours}h {minutes}min')

# Anwenden der Ticks und Labels auf die sekundäre x-Achse
ax2.set_xticks(tick_positions)
ax2.set_xticklabels(tick_labels)
ax2.set_xlabel('Vergangene Zeit', fontsize=22, labelpad=20)
ax2.tick_params(axis='both', which='major', labelsize=20)

# Plot anzeigen
plt.tight_layout()
plt.show()
