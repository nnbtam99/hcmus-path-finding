from math import ceil
import pygame as pg

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
      self.rect = pg.Rect((0, 0, self.w, self.h))

   def display(self, surface):
      pg.draw.rect(surface, pg.Color('lavender'), self.rect, 1)

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

   def display(self, surface):
      self.border.display(surface)

   def load(self, path):
      try:
         map_f = open(path, 'r')
      except:
         raise Exception('Fail to init map from \'{}\''.format(path))
         return

      try:
         self.border = Border.init_from(map_f.readline().rstrip('\n'))
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
      return self.border.get_size()
