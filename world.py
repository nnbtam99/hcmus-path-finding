import pygame as pg

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

   def run(self):
      self.display()

      while self.done == 0:
         events = pg.event.get()
         for e in events:
            if e.type == pg.QUIT:
               self.done = 1
               continue
