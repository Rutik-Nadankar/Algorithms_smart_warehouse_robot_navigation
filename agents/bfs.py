from collections import deque

def bfs(start, goal, grid):
    queue = deque([start])
    visited = {start: None}
    explored = 0

    while queue:
        current = queue.popleft()
        explored += 1

        if current == goal:
            # Goal found
            break

        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if (nx, ny) not in visited and grid.is_free(nx, ny):
                visited[(nx, ny)] = current
                queue.append((nx, ny))

    # Reconstruct path
    path = []
    node = goal
    while node:
        path.append(node)
        node = visited.get(node)

    # If goal not reached, return empty path
    if path[-1] != start:
        return [], explored

    return path[::-1], explored
