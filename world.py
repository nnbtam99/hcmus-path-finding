import pygame as pg
from algo.bfs import bfs
from algo.sa import sa_tsp

class World:
   def __init__(self, world_map, grid, size):
      self.done = 0
      self.map = world_map
      self.size = size
      self.grid = grid
      self.obs = None
      self.surface = None

   def display(self):

      # Configure window
      wnd_rect = pg.Rect(self.size)
      self.surface = pg.display.set_mode((wnd_rect.w * 40, \
                                          wnd_rect.h * 25))
      self.surface.fill(pg.Color('white'))

      # Render map and get a trace array of obstacles
      self.obs = self.map.render(self.surface, self.grid)

      # Update changes
      pg.display.update()

   def trace_path(self, path, color):

      # 8 directions, must be consistent with ones used in algorithms
      dx = [0, 0, 1, -1, 1, 1, -1, -1]
      dy = [1, -1, 0, 0, 1, -1, 1, -1]

      # Starting node and end node
      s  = self.map.S
      f  = self.map.G

      # Departed at end node, continue tracing path 
      # until we meet the starting node
      while not (f.x == s.x and f.y == s.y):

         # Get the direction of parent node
         i = path[f.y][f.x]

         # Go to parent node of f
         f.x, f.y = f.x - dx[i], f.y - dy[i]

         # Stop as soon as starting node is reached
         if f.x == s.x and f.y == s.y:
            break

         # Fill nodes in path
         self.surface.fill(color, self.grid[f.y][f.x])

         # Update changes
         pg.display.update()


   def find_path_BFS(self):
      has_path, path = bfs(self.map.S, self.map.G, \
                           self.map.border.w, self.map.border.h, self.obs)
      if not has_path:
         print('PATH: No path found')
      else:
         print('PATH: Tracing...')
         self.trace_path(path, pg.Color('skyblue'))
         print('PATH: Finish tracing path.')

   def find_path_SA(self):
      sa_tsp(self.map.S, self.map.G, \
             self.map.border.w, self.map.border.h, \
             self.obs, self.map.stops)

   def run(self):
      self.display()
      self.find_path_SA()

      while self.done == 0:
         events = pg.event.get()
         for e in events:
            if e.type == pg.QUIT:
               self.done = 1
               continue
