import sys
sys.path.append('../')
from graph import Cell
from collections import deque

# 4 directions
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

def bfs(s, f, w, h, obs):

   # Result containers 
   visited  = [[False] * w for _ in range(h)]
   path     = [[-1] * w for _ in range(h)]
   q        = deque()
   
   # Append start node to queue
   q.append(s)

   # Mark start node as visited
   visited[s.y][s.x] = True

   # Mark start node as starting point of the path
   path[s.y][s.x]    = -2
 
   while q:
      u = q.popleft()
     
      # Stop as soon as we reach the end node
      if u.x == f.x and u.y == f.y:
         break
      
      # Explore every adjacent nodes
      for i in range(len(dx)):
         x, y = u.x + dx[i], u.y + dy[i]

         # Check if the node we tend to explore is a valid node
         # and whether it has been explored
         if x in range(w) and y in range(h) and not visited[y][x]:
            visited[y][x] = True

            # Go to the node if it is not a part of obstacles
            if not obs[y][x]:
               path[y][x] = i
               q.append(Cell(x, y))

   # Return (has path, trace path container)
   if visited[f.y][f.x]:
      return True, path
   else:
      return False, None
