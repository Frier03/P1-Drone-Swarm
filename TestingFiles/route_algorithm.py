"""
    Task
        Find the shortest route to a given target node. You cannot move on a forbidden node.

    Manhattan Grid:
    
        1      2       3
        
        4      5       6
        
        7      8

@author: sh1tters#9871  
"""
from time import sleep

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

start_node: int = 1
target_node: int = 8
forbidden_nodes: list[int] = []

jumper_node: list[int] = pos_routes[start_node-1]
switcher_node: list[int] = jumper_node
node_queue: int = len(switcher_node) - 1
store_switchers = []
counter = False
tree = [jumper_node]


print('Start List: ', switcher_node)

while True:
    if target_node in switcher_node: 
        print('A possible path has been found')
        break
    else:
        if node_queue < 0:
            counter = True if len(store_switchers) > 0 else False
            
            if counter:
                print('Deleting node from switchers')
                jumper_node = store_switchers[-1]
                del store_switchers[-1]
            node_queue = len(jumper_node) - 1
            
        switcher_node = pos_routes[jumper_node[node_queue]-1]

        if not counter:
            print('Appending to switchers')
            store_switchers.append(switcher_node)
        
        node_queue -= 1
        
    tree.append(switcher_node)
        
print(tree)