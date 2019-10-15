from math import ceil
import pygame as pg

scale_pxl = 15

class Cell:
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def display(self, surface, grid, color):
      surface.fill(color, grid[self.y][self.x])

   @staticmethod
   def draw_line(cell_a, cell_b, surface, grid, color):
      dx, dy = cell_a.x - cell_b.x, cell_a.y - cell_b.y
      dx_abs, dy_abs = abs(dx), abs(dy)
      px, py = 2 * dy_abs - dx_abs, 2 * dx_abs - dy_abs

      if dx_abs > dy_abs:
         if dx < 0:
            xs, xe, y = cell_a.x, cell_b.x, cell_a.y
         else:
            xs, xe, y = cell_b.x, cell_a.x, cell_b.y

         while xs <= xe:
            surface.fill(color, grid[xs][y])
            xs += 1
            px = (px + 2 * dy_abs if px < 0 else \
                  px + 2 * (dy_abs - dx_abs))
      else:
         if dy < 0:
            ys, ye, x = cell_a.y, cell_b.y, cell_a.x
         else:
            ys, ye, x = cell_b.y, cell_a.y, cell_b.x

         while ys <= ye:
            surface.fill(color, grid[x][ys])
            ys += 1
            py = (py + 2 * dx_abs if py < 0 else \
                  py + 2 * (dx_abs - dy_abs))

   @staticmethod
   def init_from(line, delim=','):
      cells = []
      try:
         lst_coor = list(map(int, line.split(delim)))
         n_coors = int(ceil(len(lst_coor) / 2))
         for i in range(n_coors):
            x, y = lst_coor[i * 2], lst_coor[i * 2 + 1]
            cells.append(Cell(x, y))
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

   def create_grid(self):
      grid = [[pg.Rect((0, 0, scale_pxl, scale_pxl)) for j in range(self.w)] for i in range(self.h)]
      return grid

   def display(self, surface, grid, color):
      self.rect.center = surface.get_rect().center
      pg.draw.rect(surface, color, self.rect, 2)

      for i in range(self.h):
         for j in range(self.w):
            grid[i][j].x = self.rect.x + scale_pxl * j
            grid[i][j].y = self.rect.y + scale_pxl * i
            pg.draw.rect(surface, color, grid[i][j], 1)            

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

   def display(self, surface, grid, color):
      len_O = len(self.cells)
      for i in range(len_O + 1):
         Cell.draw_line(self.cells[i % len_O], \
                        self.cells[(i + 1) % len_O], \
                        surface, grid, color)

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
      self.border.display(surface, grid, pg.Color('lightsteelblue'))
      self.S.display(surface, grid, pg.Color('steelblue'))
      self.G.display(surface, grid, pg.Color('tomato'))
      for e in self.O:
         e.display(surface, grid, pg.Color('beige'))

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
      grid = self.border.create_grid()
      print('Successfully load map from \'{}\''.format(path))
      return self.border.get_size(), grid
