import numpy as np
import matplotlib.pyplot as plt

# ReLU-Aktivierungsfunktion
def relu(x):
    return np.maximum(0, x)

# Sigmoid-Aktivierungsfunktion
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Erstellen eines Bereichs von x-Werten
x = np.linspace(-8, 8, 100)

# Berechnen der y-Werte für ReLU und Sigmoid
y_relu = relu(x)
y_sigmoid = sigmoid(x)

# Schriftart zu Latin Modern ändern
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif'],
    'mathtext.fontset': 'dejavuserif'
})
# Erstellen der Plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# ReLU-Plot
ax1.plot(x, y_relu, label='ReLU', color='blue')
ax1.set_xlabel('x', fontsize=18)
ax1.set_ylabel('Aktivierung', fontsize=20)
# ax1.set_ylim(-0.1, 5)
ax1.legend(fontsize=30)
ax1.tick_params(axis='both', which='major', labelsize=16)
ax1.grid(True)

# Sigmoid-Plot
ax2.plot(x, y_sigmoid, label='Sigmoid', color='red')
ax2.set_xlabel('x', fontsize=18)
# ax2.set_ylabel('Aktivierung', fontsize=14)
# ax2.set_ylim(-0.1, 5)
ax2.legend(fontsize=30)
ax2.tick_params(axis='both', which='major', labelsize=16)
ax2.grid(True)

# Anzeigen des Plots
plt.tight_layout()
plt.show()
