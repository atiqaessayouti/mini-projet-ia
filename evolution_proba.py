import matplotlib.pyplot as plt
import numpy as np
from markov import build_markov_matrix
from astar import search

# Configuration
grid_medium = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
start = (0, 0)
goal = (4, 4)
eps = 0.2

# A* et Markov
res_astar = search(grid_medium, start, goal, 'astar')
P_mat, c_map = build_markov_matrix(grid_medium, res_astar['path'], eps)

# Initialisation pi(0)
n_states = len(P_mat)
pi = np.zeros(n_states)
start_idx = c_map[start]
goal_idx = c_map[goal]
pi[start_idx] = 1.0 # L'agent est au départ à t=0

# Calcul de pi(n) = pi(n-1) * P
n_steps = 25
prob_goal_over_time = []

for step in range(n_steps):
    prob_goal_over_time.append(pi[goal_idx])
    pi = np.dot(pi, P_mat) # Multiplication matricielle

# Visualisation
plt.figure(figsize=(8, 5))
plt.plot(range(n_steps), prob_goal_over_time, marker='o', color='purple', linestyle='-', linewidth=2)
plt.title(f"Évolution de la probabilité d'atteindre le GOAL (ε={eps})")
plt.xlabel("Nombre de pas de temps (n)")
plt.ylabel("Probabilité $\pi^{(n)}(GOAL)$")

# Ligne verticale pour montrer le temps optimal de A*
plt.axvline(x=8, color='green', linestyle='--', label='Temps optimal A* (8 pas)')

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()