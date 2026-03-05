import matplotlib.pyplot as plt
import numpy as np
from astar import search
from matplotlib.colors import ListedColormap

# 1. Définition de la grille Medium
grid_medium = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
start = (0, 0)
goal = (4, 4)

# 2. Lancement de A* pour trouver le chemin
res_astar = search(grid_medium, start, goal, 'astar')
path = res_astar['path'] if res_astar else []

# 3. Préparation de la matrice pour l'affichage (0=Blanc, 1=Noir)
grid_display = np.array(grid_medium)

plt.figure(figsize=(6, 6))
# Création des couleurs : 0 -> Blanc (Libre), 1 -> Noir (Obstacle)
cmap = ListedColormap(['white', 'black'])

# Affichage de la grille
plt.imshow(grid_display, cmap=cmap, origin='upper')

# Dessiner les lignes du quadrillage
plt.grid(which='major', axis='both', linestyle='-', color='gray', linewidth=2)
plt.xticks(np.arange(-0.5, 5, 1), [])
plt.yticks(np.arange(-0.5, 5, 1), [])

# Tracer le chemin optimal trouvé par A*
if path:
    y_coords = [p[0] for p in path]
    x_coords = [p[1] for p in path]
    plt.plot(x_coords, y_coords, marker='o', color='dodgerblue', linewidth=3, markersize=8, label='Chemin optimal (A*)')

# Marquer le point de départ et d'arrivée
plt.plot(start[1], start[0], marker='s', color='limegreen', markersize=14, label='Départ $s_0$ (0,0)')
plt.plot(goal[1], goal[0], marker='*', color='crimson', markersize=18, label='But $g$ (4,4)')

plt.title("Environnement : Grille 'Medium' et Plan Déterministe")
# Placer la légende en bas
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3)

plt.tight_layout()
plt.show()