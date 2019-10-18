import sys
sys.path.append('../')
from graph import Cell
<<<<<<< HEAD
from collections import deque

# 4 directions
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

def dfs(s, f, w, h, obs):

   # Result containers 
   visited  = [[False] * w for _ in range(h)]
   path     = [[-1] * w for _ in range(h)]
   q        = deque()
   
   # Append start node to queue
   q.append(s)
=======

# 8 directions
dx = [0, 0, 1, -1, 1, 1, -1, -1]
dy = [1, -1, 0, 0, 1, -1, 1, -1]

def dfs(s, f, w, h, obs):
    
   # Result containers 
   visited  = [[False] * w for _ in range(h)]
   path     = [[-1] * w for _ in range(h)]
   stack        = []
   
   # Append start node to stack
   stack.append(s)
>>>>>>> ca4a79b0c4c146bb5b97a1d5a9b5049280553af7

   # Mark start node as visited
   visited[s.y][s.x] = True

   # Mark start node as starting point of the path
   path[s.y][s.x]    = -2
 
<<<<<<< HEAD
   while q:
      u = q.pop()
=======
   while len(stack) > 0:
      u = stack.pop()
>>>>>>> ca4a79b0c4c146bb5b97a1d5a9b5049280553af7
     
      # Stop as soon as we reach the end node
      if u.x == f.x and u.y == f.y:
         break
      
<<<<<<< HEAD
      # Explore every adjancent nodes
      for i in range(len(dx)):
         x, y = u.x + dx[i], u.y + dy[i]

         # Check if the node we tends to explore is a valid node
=======
      # Explore every adjacent nodes
      for i in range(len(dx)):
         x, y = u.x + dx[i], u.y + dy[i]

         # Check if the node we tend to explore is a valid node
>>>>>>> ca4a79b0c4c146bb5b97a1d5a9b5049280553af7
         # and whether it has been explored
         if x in range(w) and y in range(h) and not visited[y][x]:
            visited[y][x] = True

            # Go to the node if it is not a part of obstacles
            if not obs[y][x]:
               path[y][x] = i
<<<<<<< HEAD
               q.append(Cell(x, y))
=======
               stack.append(Cell(x, y))
>>>>>>> ca4a79b0c4c146bb5b97a1d5a9b5049280553af7

   # Return (has path, trace path container)
   if visited[f.y][f.x]:
      return True, path
   else:
<<<<<<< HEAD
      return False, None
=======
      return False, None
>>>>>>> ca4a79b0c4c146bb5b97a1d5a9b5049280553af7
