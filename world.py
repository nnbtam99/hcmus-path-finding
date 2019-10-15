import pygame as pg

class World:
   def __init__(self, world_map, grid, size):
      self.done = False
      self.m = world_map
      self.size = size
      self.grid = grid
      self.surface = None

   def display(self):
      wnd_rect = pg.Rect(self.size)
      self.surface = pg.display.set_mode((wnd_rect.w * 40, \
                                          wnd_rect.h * 25))
      self.surface.fill(pg.Color('white'))
      self.m.display(self.surface, self.grid)
      pg.display.update()
