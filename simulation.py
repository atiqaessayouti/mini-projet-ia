import random
from astar import get_neighbors

def simulate_trajectories(grid, path, goal, epsilon, n_sims=1000):
    """Simuler N trajectoires et estimer P(atteindre GOAL) [cite: 64, 65]"""
    if not path: return 0.0
    success_count = 0
    policy = {path[i]: path[i+1] for i in range(len(path)-1)}
    
    for _ in range(n_sims):
        current = path[0]
        steps = 0
        while current != goal and steps < 100:
            if current not in policy: break
            if random.random() > epsilon: current = policy[current]
            else:
                neighbors = get_neighbors(current, grid)
                if neighbors: current = random.choice(neighbors)
            steps += 1
        if current == goal: success_count += 1
    return (success_count / n_sims) * 100