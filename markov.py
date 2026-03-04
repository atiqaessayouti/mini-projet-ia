import numpy as np
from astar import get_neighbors

def build_markov_matrix(grid, path, epsilon):
    """Construction de la matrice P stochastique [cite: 9, 27]"""
    free_cells = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 0]
    cell_to_idx = {cell: i for i, cell in enumerate(free_cells)}
    n = len(free_cells)
    P = np.zeros((n, n))
    policy = {path[i]: path[i+1] for i in range(len(path)-1)}
    
    for i, cell in enumerate(free_cells):
        if cell == path[-1]: # GOAL est absorbant [cite: 35]
            P[i, i] = 1.0
            continue
        if cell in policy:
            target = policy[cell]
            P[i, cell_to_idx[target]] = 1.0 - epsilon # Action voulue [cite: 32]
            neighbors = get_neighbors(cell, grid)
            others = [nb for nb in neighbors if nb != target]
            if others:
                for nb in others: P[i, cell_to_idx[nb]] = epsilon / len(others) # Déviation [cite: 32]
            else: P[i, i] += epsilon
        else: P[i, i] = 1.0 # FAIL absorbant [cite: 36]
    return P, cell_to_idx

def analyze_absorption(P, cell_to_idx, start, goal):
    """Calcul des probabilités d'absorption et temps moyen [cite: 36, 61]"""
    n = P.shape[0]
    goal_idx = cell_to_idx[goal]
    absorbing = [i for i in range(n) if np.isclose(P[i, i], 1.0)]
    transient = [i for i in range(n) if i not in absorbing]
    
    if cell_to_idx[start] in absorbing: return 0.0, (1.0 if cell_to_idx[start] == goal_idx else 0.0)

    Q = P[np.ix_(transient, transient)]
    R = P[np.ix_(transient, absorbing)]
    I = np.eye(Q.shape[0])
    
    try:
        N = np.linalg.inv(I - Q) # Matrice fondamentale [cite: 39]
        t = np.sum(N, axis=1)
        B = np.dot(N, R)
        start_idx_transient = transient.index(cell_to_idx[start])
        goal_idx_absorbing = absorbing.index(goal_idx)
        return t[start_idx_transient], B[start_idx_transient, goal_idx_absorbing]
    except np.linalg.LinAlgError: return 0.0, 0.0