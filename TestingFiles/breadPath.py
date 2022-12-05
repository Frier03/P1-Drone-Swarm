"""
https://en.wikipedia.org/wiki/Breadth-first_search
Peters ide med JUICED THE FUCK OP 
        1      2       3
        
        4      5       6
        
        7      8
"""

pos_routes: list[int] = [ # Possible route combinations
        [2, 4], # Node 1
        [1, 5, 3], # Node 2
        [2, 6], # Node 3
        [1, 5, 7], # Node 4
        [2, 4, 8, 6], # Node 5
        [3, 5], # Node 6
        [4, 8], # Node 7
        [5, 7] # Node 8
    ]
bQueue = 0

def bfs(start, target):
    queue = [ [start] ]
    seen = [start]

    while queue:
        path = queue.pop(0)
        print(path)
        if path[-1] == target:
            return path
        for nextPaths in pos_routes[path[-1] - 1]:
            if nextPaths not in seen:
                print("Appending", path + [nextPaths])
                queue.append(path + [nextPaths])
                seen.append(nextPaths)
        

print("Found path =", bfs(1, 8))


