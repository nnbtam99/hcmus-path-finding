import sys
sys.path.append('../')
from graph import Cell
from heapq import heappush, heappop, heapify


INF      = int(1e9)
dx       = [0, 0, 1, -1]
dy       = [1, -1, 0, 0]
weights  = [1, 1, 1, 1]


class DStar:
   def __init__(self, s, f, w, h, restricted):
      self.s         = Cell(x=s.x, y=s.y)
      self.f         = Cell(x=f.x, y=f.y)
      self.w         = w
      self.h         = h

      self.dirs      = [[-1] * w for _ in range(h)]
      self.dist      = [[INF] * w for _ in range(h)]
      self.rhs       = [[INF] * w for _ in range(h)]
      self.pq        = []
      self.k_m       = 0

      # Set 0 as lookahead value from end node to itself
      self.rhs[f.y][f.x] = 0

      # Push end node and its key value to priority queue
      heappush(self.pq, (self.get_key(f), f))

      # Pre-compute shortest path on initial map
      self.run(restricted=restricted)

   @staticmethod
   def heuristic(u, v):
      dx, dy         = abs(u.x - v.x), abs(u.y - v.y)
      return dx + dy

   """
   Priority: tuple (f(x), g(x)) where f(x) = g(x) + h(x)
   g_rhs ~ g(x): cost function
   DStar.heuristic ~ h(x): heuristic function
   """
   def get_key(self, u):
      g_rhs          = min(self.dist[u.y][u.x], self.rhs[u.y][u.x])
      return (g_rhs + self.k_m + DStar.heuristic(u, self.s), g_rhs)

   def get_rhs(self, u, restricted):
      min_cost       = INF

      for i in range(len(dx)):
         x, y        = u.x + dx[i], u.y + dy[i]

         if x in range(self.w) and y in range(self.h) and not restricted[y][x]:
            cost     = self.dist[y][x] + Cell.distance(u, Cell(x=x, y=y))
            if cost < min_cost:
               min_cost = cost
               self.dirs[u.y][u.x] = i
       
      return min_cost

   def update_vertices(self, u, restricted, inclusive=False):
      if inclusive:
         self.update(u, restricted)

      for i in range(len(dx)):
         x, y        = u.x + dx[i], u.y + dy[i]

         if x in range(self.w) and y in range(self.h) and not restricted[y][x]:
            self.update(Cell(x=x, y=y), restricted)


   """
   Update rhs-value and keys of vertices that potentially affected
   by either changed edge costs or membership in priority queue
   if its state changed (locally consistent <-> inconsistent)
   """
   def update(self, u, restricted):
      if u.x != self.f.x or u.y != self.f.y:
         self.rhs[u.y][u.x]   = self.get_rhs(u, restricted)

      if u in self.pq:
         self.pq.remove(u)
         self.pq     = heapify(self.pq)

      if self.dist[u.y][u.x] != self.rhs[u.y][u.x]:
         heappush(self.pq, (self.get_key(u), u))

   def run(self, restricted):
      x, y           = self.s.x, self.s.y

      while self.pq and (self.pq[0][0] < self.get_key(self.s) or self.dist[y][x] != self.rhs[y][x]):
         """
         Inconsistent nodes go on the priority queue for processing
         - Consistent: g(u) = rhs(u)
         - Inconsistent: g(u) != rhs(u)
         """
         k_old, u    = heappop(self.pq)
         k_new       = self.get_key(u)
        
         if k_old < k_new:
            heappush(self.pq, (k_new, u))

         elif self.dist[u.y][u.x] > self.rhs[u.y][u.x]:
            """
            Check if the vertex u is locally overconsistent
            where g(u) > rhs(u)
            """
            self.dist[u.y][u.x]  = self.rhs[u.y][u.x]
            self.update_vertices(u, restricted)
         
         else:
            """
            A vertex u is either locally consistent or underconsistent
            So, make it overconsistent and propagate changed costs to neighboring nodes
            """ 
            self.dist[u.y][u.x]  = INF
            self.update_vertices(u, restricted, inclusive=True)

      i = self.dirs[y][x]
      print(i)
      self.s.x -= dx[i]
      self.s.y -= dy[i]
      return self.s
