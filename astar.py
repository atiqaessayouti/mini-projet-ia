import heapq
import time

def manhattan(p, goal):
    """Heuristique Manhattan: h(n) = |xn - xg| + |yn - yg|"""
    return abs(p[0] - goal[0]) + abs(p[1] - goal[1])

def get_neighbors(state, grid):
    """L-jiran (4-voisins) li machi obstacles"""
    x, y = state
    neighbors = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def search(grid, start, goal, mode='astar'):
    """Implémentation A*, UCS, et Greedy"""
    start_time = time.time()
    open_list = []
    h_start = manhattan(start, goal) if mode != 'ucs' else 0
    heapq.heappush(open_list, (h_start, 0, start, []))
    
    closed_list = set()
    nodes_expanded = 0
    
    while open_list:
        f, g, current, path = heapq.heappop(open_list)
        if current in closed_list: continue
        nodes_expanded += 1
        
        if current == goal:
            return {"path": path + [current], "cost": g, "nodes": nodes_expanded, "time": time.time() - start_time}
            
        closed_list.add(current)
        for neighbor in get_neighbors(current, grid):
            if neighbor not in closed_list:
                new_g = g + 1 
                new_h = manhattan(neighbor, goal) if mode != 'ucs' else 0
                if mode == 'astar': f_n = new_g + new_h
                elif mode == 'ucs': f_n = new_g
                elif mode == 'greedy': f_n = new_h
                heapq.heappush(open_list, (f_n, new_g, neighbor, path + [current]))
    return None