import sys
sys.path.append('../')
from graph import Cell, Map
from collections import deque

# 4 directions
dx       = [0, 0, 1, -1]
dy       = [1, -1, 0, 0]
weight   = [1, 1, 1, 1]

def dfs(s, f, w, h, restricted):

   # Containers 
   visited  = [[False] * w for _ in range(h)]
   dist     = [[-1] * w for _ in range(h)]
   dirs     = [[-1] * w for _ in range(h)]
   stack    = deque()
   
   # Append start node to queue
   stack.append(s)

   """
   Mart start node as visted node
   Set 0 as cost of the current shortest path from start node to itself 
   Set -2 as direction to the parent node on the shortest path from start node
   """
   visited[s.y][s.x] = True
   dist[s.y][s.x]    = 0
   dirs[s.y][s.x]    = -2
 
   while stack:
      u              = stack.pop()
     
      # Stop as soon as we reached end node
      if u.x == f.x and u.y == f.y:
         break
      
      # Explore every adjacent nodes
      for i in range(len(dx)):
         x, y        = u.x + dx[i], u.y + dy[i]

         # Check if the node we're about to explore is a valid node
         # and whether it has been previously explored
         if x in range(w) and y in range(h) and not visited[y][x]:
            visited[y][x]     = True

            # Go to the node if it is not restricted
            if not restricted[y][x]:
               dist[y][x]     = weight[i] + dist[u.y][u.x]
               dirs[y][x]     = i
               stack.append(Cell(x=x, y=y))

   path = None
   cost = -1

   if visited[f.y][f.x]:
      path     = Map.trace_path_by_dir(s=s, f=f, dirs=dirs)
      cost     = dist[f.y][f.x]
   
   return visited[f.y][f.x], cost, path
