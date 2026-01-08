import heapq

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal, grid):
    pq = []
    heapq.heappush(pq, (0, start))
    came_from = {start: None}
    cost = {start: 0}
    explored = 0

    while pq:
        _, current = heapq.heappop(pq)
        explored += 1

        if current == goal:
            break

        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if not grid.is_free(nx, ny):
                continue

            new_cost = cost[current] + 1
            if (nx, ny) not in cost or new_cost < cost[(nx, ny)]:
                cost[(nx, ny)] = new_cost
                priority = new_cost + heuristic((nx, ny), goal)
                heapq.heappush(pq, (priority, (nx, ny)))
                came_from[(nx, ny)] = current

    # Reconstruct path
    path = []
    node = goal
    while node:
        path.append(node)
        node = came_from.get(node)

    # If goal not reached, return empty path
    if path[-1] != start:
        return [], explored

    return path[::-1], explored
