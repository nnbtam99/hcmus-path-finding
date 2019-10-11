from math import ceil

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
   def __init__(self, path):
      self.border = None
      self.S = self.G = None
      self.O = []
      try:
         self.load(path)
         print('Successfully load map from \'{}\''.format(path))
      except Exception as e:
         raise Exception(str(e))
         return

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
         n_O = int(map_f.readline().rstrip('\n'))
         for _ in range(n_O):
            self.O.append(Obstacle.init_from(map_f.readline(). \
                                             rstrip('\n')))
      except:
         raise Exception('Wrong map format')
      
      map_f.close()
