import sys
sys.path.append('../')
from graph import Cell
from collections import deque

dx = [0, 0, 1, -1, 1, 1, -1, -1]
dy = [1, -1, 0, 0, 1, -1, 1, -1]

def bfs(s, f, obs):
   h, w = len(obs), len(obs[0])
   visited = [[False] * w for _ in range(h)]
   path = [[-1] * w for _ in range(h)]
   q = deque()
   
   q.append(s)
   visited[s.y][s.x] = True
   path[s.y][s.x] = -1 
 
   while q:
      u = q.popleft()
      
      if u.x == f.x and u.y == f.y:
         break

      for i in range(len(dx)):
         x, y = u.x + dx[i], u.y + dy[i]
         if x in range(w) and y in range(h) and not visited[y][x]:
            visited[y][x] = True
            if not obs[y][x]:
               path[y][x] = i
               q.append(Cell(x, y))

   if visited[f.y][f.x]:
      return True, path
   else:
      return False, None

   
