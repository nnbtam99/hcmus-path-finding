import pygame as pg
from algo.bfs import bfs

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

      # Render map and get a 2D trace array of obstacles
      self.obs = self.map.render(self.surface, self.grid)

      # Update changes
      pg.display.update()

   def trace_path(self, path, color):
      dx = [0, 0, 1, -1, 1, 1, -1, -1]
      dy = [1, -1, 0, 0, 1, -1, 1, -1]
      f = self.map.G
      s = self.map.S

      while not (f.x == s.x and f.y == s.y):
         i = path[f.y][f.x]
         f.x, f.y = f.x - dx[i], f.y - dy[i]
         if f.x == s.x and f.y == s.y:
            break
         self.surface.fill(color, self.grid[f.y][f.x])
         pg.display.update()

   def find_path_BFS(self):
      accessible, path = bfs(self.map.S, self.map.G, self.obs)
      if not accessible:
         print('No path found')
      else:
         print('Tracing path...')
         self.trace_path(path, pg.Color('skyblue'))

   def run(self):
      self.display()
      self.find_path_BFS()

      while self.done == 0:
         events = pg.event.get()
         for e in events:
            if e.type == pg.QUIT:
               self.done = 1
               continue
