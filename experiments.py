from astar import search
from markov import build_markov_matrix, analyze_absorption
from simulation import simulate_trajectories
import matplotlib.pyplot as plt

# ==========================================
# 1. DÉFINITION DES GRILLES
# ==========================================
grid_easy = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]

grid_medium = [
    [0,0,0,0,0],
    [0,1,1,1,0],
    [0,0,0,1,0],
    [0,1,0,0,0],
    [0,0,0,0,0]
]

grid_hard = [
    [0,1,0,0,0],
    [0,1,0,1,0],
    [0,1,0,1,0],
    [0,0,0,1,0],
    [1,1,0,0,0]
]

start = (0, 0)
goal = (4, 4)
modes = ['ucs', 'greedy', 'astar']

print("======================================================")
print("🚀 DÉBUT DES EXPÉRIENCES - PLANIFICATION ROBUSTE (IA)")
print("======================================================\n")

# ======================================================
# PARTIE 1 : COMPARAISON DES ALGORITHMES (3 Grilles)
# ======================================================
print("--- PARTIE 1 : Comparaison des Algorithmes (Terminal) ---")

nodes_data = {'easy': [], 'medium': [], 'hard': []}
time_data = {'easy': [], 'medium': [], 'hard': []}
cost_data = {'easy': [], 'medium': [], 'hard': []}

for mode in modes:
    res_e = search(grid_easy, start, goal, mode)
    res_m = search(grid_medium, start, goal, mode)
    res_h = search(grid_hard, start, goal, mode)
    
    nodes_data['easy'].append(res_e['nodes'] if res_e else 0)
    nodes_data['medium'].append(res_m['nodes'] if res_m else 0)
    nodes_data['hard'].append(res_h['nodes'] if res_h else 0)
    
    time_data['easy'].append(res_e['time']*1000 if res_e else 0)
    time_data['medium'].append(res_m['time']*1000 if res_m else 0)
    time_data['hard'].append(res_h['time']*1000 if res_h else 0)
    
    cost_data['easy'].append(res_e['cost'] if res_e else 0)
    cost_data['medium'].append(res_m['cost'] if res_m else 0)
    cost_data['hard'].append(res_h['cost'] if res_h else 0)

# Création de la figure pour la Partie 1 (3 sous-graphes alignés)
fig1, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
fig1.suptitle("Expérience 1 : Comparaison des algorithmes sur 3 grilles (Easy, Medium, Hard)")

ax1.plot(modes, nodes_data['easy'], marker='o', label="Easy")
ax1.plot(modes, nodes_data['medium'], marker='o', label="Medium")
ax1.plot(modes, nodes_data['hard'], marker='o', label="Hard")
ax1.set_title("Nœuds développés")
ax1.set_ylabel("Nombre de nœuds")
ax1.legend()
ax1.grid(True)

ax2.plot(modes, time_data['easy'], marker='o', label="Easy")
ax2.plot(modes, time_data['medium'], marker='o', label="Medium")
ax2.plot(modes, time_data['hard'], marker='o', label="Hard")
ax2.set_title("Temps d'exécution (ms)")
ax2.set_ylabel("Temps (ms)")
ax2.legend()
ax2.grid(True)

ax3.plot(modes, cost_data['easy'], marker='o', label="Easy")
ax3.plot(modes, cost_data['medium'], marker='o', label="Medium")
ax3.plot(modes, cost_data['hard'], marker='o', label="Hard")
ax3.set_title("Coût du chemin")
ax3.set_ylabel("Coût")
ax3.legend()
ax3.grid(True)

# ======================================================
# PARTIE 2 : IMPACT DE L'INCERTITUDE (Grille Medium)
# ======================================================
print("\n--- PARTIE 2 : Impact de l'incertitude (Markov & Monte Carlo) ---")
print("Analyse focalisée sur la Grille 'Medium'\n")

res_astar_medium = search(grid_medium, start, goal, 'astar')
epsilons = [0.0, 0.1, 0.2, 0.3]
prob_mc = []
prob_markov = []
temps_moyen = []

print(f"{'Epsilon':<8} | {'Simu Monte-Carlo':<20} | {'Markov Théorie':<15} | {'E(pas)':<8}")
print("-" * 65)

if res_astar_medium:
    for eps in epsilons:
        # Monte Carlo
        sim_success = simulate_trajectories(grid_medium, res_astar_medium['path'], goal, eps, n_sims=1000)
        prob_mc.append(sim_success / 100)
        
        # Markov Théorie
        P_mat, c_map = build_markov_matrix(grid_medium, res_astar_medium['path'], eps)
        t_avg, prob_th = analyze_absorption(P_mat, c_map, start, goal)
        prob_markov.append(prob_th)
        temps_moyen.append(t_avg)
        
        print(f"{eps:<8.1f} | {sim_success:>15.1f}% | {prob_th*100:>13.1f}% | {t_avg:>6.1f}")

# Création de la figure pour la Partie 2 (2 sous-graphes)
fig2, (ax4, ax5) = plt.subplots(1, 2, figsize=(12, 5))
fig2.suptitle("Expérience 2 : Robustesse du plan A* face à l'incertitude (Grille Medium)")

ax4.plot(epsilons, prob_mc, marker='s', label="Monte Carlo")
ax4.plot(epsilons, prob_markov, marker='^', label="Markov Théorie")
ax4.set_title("Probabilité d'atteindre le GOAL")
ax4.set_xlabel("Epsilon (ε)")
ax4.set_ylabel("Probabilité")
ax4.legend()
ax4.grid(True)

ax5.plot(epsilons, temps_moyen, marker='o', color='red')
ax5.set_title("Temps moyen avant absorption")
ax5.set_xlabel("Epsilon (ε)")
ax5.set_ylabel("Temps moyen E(pas)")
ax5.grid(True)

# ======================================================
# PARTIE 3 : HEATMAP (Matrice de Transition)
# ======================================================
print("\n--- PARTIE 3 : Génération de la Heatmap (ε = 0.2) ---")
eps_vis = 0.2
if res_astar_medium:
    P_mat_vis, _ = build_markov_matrix(grid_medium, res_astar_medium['path'], eps_vis)
    
    plt.figure(figsize=(7, 6))
    plt.imshow(P_mat_vis, cmap='Blues', interpolation='nearest')
    plt.colorbar(label='Probabilité de transition')
    plt.title(f"Heatmap de la Matrice de Transition P (ε = {eps_vis})")
    plt.xlabel("Index de l'état d'arrivée")
    plt.ylabel("Index de l'état de départ")

print("\n✅ Expériences terminées avec succès ! Affichage des graphiques...")
# Affiche toutes les fenêtres en même temps proprement
plt.show()
# ======================================================
# PARTIE 3 : HEATMAP ET AFFICHAGE (Matrice de Transition)
# ======================================================
print("\n--- PARTIE 3 : Génération et Affichage de la Matrice P (ε = 0.2) ---")
eps_vis = 0.2
if res_astar_medium:
    P_mat_vis, _ = build_markov_matrix(grid_medium, res_astar_medium['path'], eps_vis)
    
    # ZIDNA HADI: Bach t-tbe3 l-matrice f-Terminal b-tariqa nqiya
    print("\nMatrice de Transition P (valeurs numériques arrondies) :")
    for row in P_mat_vis:
        # K-n-khliwha t-ban b-jouj arqam mor l-fasila (ex: 0.80)
        formatted_row = ["{:.2f}".format(val) for val in row]
        print(" ".join(formatted_row))
    
    # L-Graphe Heatmap
    plt.figure(figsize=(7, 6))
    plt.imshow(P_mat_vis, cmap='Blues', interpolation='nearest')
    plt.colorbar(label='Probabilité de transition')
    plt.title(f"Heatmap de la Matrice de Transition P (ε = {eps_vis})")
    plt.xlabel("Index de l'état d'arrivée")
    plt.ylabel("Index de l'état de départ")

print("\n✅ Expériences terminées avec succès ! Affichage des graphiques...")
# Affiche toutes les fenêtres en même temps proprement
plt.show()