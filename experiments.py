from astar import search
from markov import build_markov_matrix, analyze_absorption
from simulation import simulate_trajectories
import matplotlib.pyplot as plt

# Grille d'exemple
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
start, goal = (0, 0), (4, 4)

print("=== EXPÉRIENCE E.1: Comparaison des algorithmes ===")
print(f"{'Mode':<10} | {'Coût':<5} | {'Nœuds':<6} | {'Temps(s)':<8}")
print("-" * 40)
for mode in ['ucs', 'greedy', 'astar']:
    res = search(grid, start, goal, mode)
    if res:
        print(f"{mode:<10} | {res['cost']:<5} | {res['nodes']:<6} | {res['time']:.5f}")

print("\n=== EXPÉRIENCE E.2: Impact de l'incertitude sur A* ===")
res_astar = search(grid, start, goal, 'astar')
if res_astar:
    print(f"{'Epsilon':<8} | {'Simu Monte-Carlo':<20} | {'Markov Théorie':<15} | {'E(pas)':<8}")
    print("-" * 65)
    for eps in [0, 0.1, 0.2, 0.3]:
        sim_success = simulate_trajectories(grid, res_astar['path'], goal, eps, n_sims=1000)
        P_mat, c_map = build_markov_matrix(grid, res_astar['path'], eps)
        t_avg, prob_th = analyze_absorption(P_mat, c_map, start, goal)
        print(f"{eps:<8.1f} | {sim_success:>15.1f}% | {prob_th*100:>13.1f}% | {t_avg:>6.1f}")
        

print("\n=== EXPÉRIENCE E.3: Graph ε vs Probabilité ===")

epsilons = [0.0, 0.1, 0.2, 0.3]
prob_mc = []
prob_markov = []

if res_astar:
    for eps in epsilons:
        sim_success = simulate_trajectories(
            grid,
            res_astar['path'],
            goal,
            eps,
            n_sims=1000
        )

        P_mat, c_map = build_markov_matrix(
            grid,
            res_astar['path'],
            eps
        )

        t_avg, prob_th = analyze_absorption(
            P_mat,
            c_map,
            start,
            goal
        )

        prob_mc.append(sim_success / 100)
        prob_markov.append(prob_th)

plt.figure()
plt.plot(epsilons, prob_mc)
plt.plot(epsilons, prob_markov)

plt.xlabel("Epsilon (ε)")
plt.ylabel("Probabilité d'atteindre GOAL")
plt.title("Impact de l'incertitude sur la robustesse du plan (A*)")
plt.legend(["Monte Carlo", "Markov Théorie"])
plt.grid(True)
plt.show()