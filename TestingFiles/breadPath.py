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
paths = []

def bfs(start, target, disabledSpots=[]):
    queue = [ [start] ]
    seen = [start]

    while queue:
        path = queue.pop(0)
        paths.append(path)
        print("path =", path)
        if path[-1] == target: return path
        for nextPaths in pos_routes[path[-1] - 1]:
            if nextPaths not in seen and nextPaths not in disabledSpots:
                queue.append(path + [nextPaths])
                seen.append(nextPaths)

start = 1
target = 6
disabledSpots = [2, 5]
print("Finding path from", start, "to", target)
print("Blocked spots are", disabledSpots)
foundPath = bfs(start, target, disabledSpots)

print("Found path =", foundPath)
if foundPath == None:
    print("Path is blocked")
    bestAlternative = ([1, 1, 1, 1], 9)    #Path, distance
    for p in paths:
        xRow = (p[-1]-1)//3 - (target-1)//3
        yRow = (p[-1]-1) % 3 - (target-1) % 3
        distance = abs(xRow) + abs(yRow)
        print(p, "has distance", distance)
        if distance < bestAlternative[1]:
            bestAlternative = (p, distance)
        elif distance == bestAlternative and len(p) < len( bestAlternative[0] ):
            bestAlternative = (p, distance)
                
                
    print("Best Alt", bestAlternative[0], "dist:", bestAlternative[1])



