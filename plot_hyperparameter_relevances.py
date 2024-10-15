import matplotlib.pyplot as plt

# Daten
hyperparameters = [
    'activation_fn', 'batch_size', 'clip_range', 'ent_coef', 'gae_lambda', 
    'gamma', 'learning_rate', 'log_std_init', 'lr_schedule', 'max_grad_norm',
    'n_epochs', 'n_steps', 'net_arch', 'ortho_init', 'sde_sample_freq', 'vf_coef'
]
relevance = [
    0.00, 0.01, 0.09, 0.02, 0.03, 
    0.04, 0.15, 0.07, 0.01, 0.04, 
    0.04, 0.04, 0.03, 0.03, 0.06, 0.20
]

# Schriftart zu Latin Modern ändern
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif'],
    'mathtext.fontset': 'dejavuserif'
})

bar_width = 0.8  # Breite der Balken anpassen

# Plot erstellen
fig, ax = plt.subplots(figsize=(10, 10))
ax.barh(hyperparameters, relevance, color='steelblue', height=bar_width)

# Werte auf den Balken anzeigen
for index, value in enumerate(relevance):
    ax.text(value + 0.005, index, f'{value:.2f}', va='center', fontsize=22)

# Achsenbeschriftungen und Titel
ax.set_xlabel('Hyperparameter Relevanz', fontsize=26, labelpad=20)

# Schriftgröße der Hyperparameter vergrößern
# Schriftgröße der Hyperparameter und x-Achsen-Ticks vergrößern
ax.tick_params(axis='y', labelsize=22)
ax.tick_params(axis='x', labelsize=24)  # Schriftgröße der x-Achsen-Ticks vergrößern

# Plot-Rand entfernen
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Layout anpassen
plt.tight_layout()

# Plot anzeigen
plt.show()
