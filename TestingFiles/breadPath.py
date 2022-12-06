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

def bfs(start, target, disabledSpots=[]):
    queue = [ [start] ]
    seen = [start]
    allPaths = []          #Saves all paths

    # ORIGINAL BREAD'th algorithm
    while queue:
        path = queue.pop(0)
        allPaths.append(path)
        if path[-1] == target: return (path, 0)
        for nextPaths in pos_routes[path[-1] - 1]:
            if nextPaths not in seen and nextPaths not in disabledSpots:
                queue.append(path + [nextPaths])
                seen.append(nextPaths)
    
    # Expanded Bread. Nearest spot if no path found
    # Path is blocked
    nearestPath = ([1, 1, 1, 1], 9)    #Path, distance
    for p in allPaths:
        xRow = (p[-1]-1)//3 - (target-1)//3
        yRow = (p[-1]-1) % 3 - (target-1) % 3
        dist = abs(xRow) + abs(yRow)
        if dist < nearestPath[1]:
            nearestPath = (p, dist)
        elif dist == nearestPath and len(p) < len( nearestPath[0] ):
            nearestPath = (p, dist)
    return nearestPath




start = 2
target = 5
disabledSpots = [5]
print("Finding path from", start, "to", target)
print("Blocked spots are", disabledSpots)
foundPath = bfs(start, target, disabledSpots)
print("[+] Found path =", foundPath)





