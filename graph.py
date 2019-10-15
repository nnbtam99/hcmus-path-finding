from math import ceil
import pygame as pg

scale_pxl = 15

class Cell:
   def __init__(self, r, c):
      self.r = r
      self.c = c

   @staticmethod
   def init_from(line, delim=','):
      cells = []
      try:
         lst_coor = list(map(int, line.split(delim)))
         n_coors = int(ceil(len(lst_coor) / 2))
         for i in range(n_coors):
            r, c = lst_coor[i * 2], lst_coor[i * 2 + 1]
            cells.append(Cell(r, c))
      except:
         raise Exception('Fail to init cell from line \'{}\'' \
                        .format(line))
         return

      return cells

class Border:
   def __init__(self, w, h):
      self.w = w
      self.h = h
      self.rect = pg.Rect((0, 0, self.w * scale_pxl, self.h * scale_pxl))

   def pool_grid(self):
      grid = [[pg.Rect((0, 0, scale_pxl, scale_pxl)) for j in range(self.w)] for i in range(self.h)]
      return grid

   def display(self, surface, grid):
      self.rect.center = surface.get_rect().center
      pg.draw.rect(surface, pg.Color('mediumseagreen'), self.rect, 2)

      for i in range(self.h):
         for j in range(self.w):
            grid[i][j].x = self.rect.x + scale_pxl * j
            grid[i][j].y = self.rect.y + scale_pxl * i
            pg.draw.rect(surface, pg.Color('mediumseagreen'), grid[i][j], 1)            

   def get_size(self):
      return (0, 0, self.w, self.h)

   @staticmethod
   def init_from(line, delim=','): 
      try:
         w, h = map(int, line.split(delim))
         new_border = Border(w, h)
      except:
         raise Exception('Fail to init border from line \'{}\'' \
                        .format(line))
         return

      return new_border

class Obstacle:
   def __init__(self, cells):
      self.cells = cells

   @staticmethod
   def init_from(line, delim=','):
      try:
         cells = Cell.init_from(line, delim)
         new_obstacle = Obstacle(cells)
      except:
         raise Exception('Fail to init obstacle from line \'{}\'' \
                         .format(line))
         return
   
      return new_obstacle

class Map:
   def __init__(self):
      self.border = None
      self.S = self.G = None
      self.O = []

   def display(self, surface, grid):
      self.border.display(surface, grid)


   def load(self, path):
      try:
         map_f = open(path, 'r')
      except:
         raise Exception('Fail to init map from \'{}\''.format(path))
         return

      try:
         self.border = Border.init_from(map_f.readline().rstrip('\n'))
         grid = self.border.pool_grid()
         self.S, self.G = tuple(Cell.init_from(map_f.readline(). \
                                               rstrip('\n')))
         len_O = int(map_f.readline().rstrip('\n'))
         for _ in range(len_O):
            self.O.append(Obstacle.init_from(map_f.readline(). \
                                             rstrip('\n')))
      except Exception as e:
         raise Exception('MapError: {}'.format(e))
      
      map_f.close()
      print('Successfully load map from \'{}\''.format(path))
      return self.border.get_size(), grid
