import matplotlib.pyplot as plt

# ==========================================
# Graphe Circulaire : Écart Théorie vs Simulation (ε = 0.3)
# ==========================================

# Données pour Epsilon = 0.3 (issues des résultats de l'Expérience 2)
labels = ['Succès\n(Atteint GOAL)', 'Échec\n(Déviation / Perdu)']

# Valeurs Monte Carlo (Simulation)
mc_success = 73.6
mc_fail = 100 - mc_success
sizes_mc = [mc_success, mc_fail]

# Valeurs Markov (Théorie stricte)
markov_success = 47.1
markov_fail = 100 - markov_success
sizes_markov = [markov_success, markov_fail]

# Couleurs : Vert pour le succès, Rouge pour l'échec
colors = ['#2ca02c', '#d62728'] 
# Faire ressortir la part de succès (effet 3D léger)
explode = (0.1, 0) 

# Création de la figure avec 2 sous-graphes (1 ligne, 2 colonnes)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle("Comparaison des Taux de Réussite face à une forte incertitude (ε = 0.3)", fontsize=14, fontweight='bold')

# Pie chart 1 : Monte Carlo
ax1.pie(sizes_mc, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.set_title("Simulation Monte-Carlo\n(Approche Flexible)")

# Pie chart 2 : Markov
ax2.pie(sizes_markov, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
ax2.set_title("Théorie Markovienne\n(Approche Stricte)")

# Affichage
plt.tight_layout()
plt.show()