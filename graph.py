from math import ceil
import pygame as pg

scale_pxl = 15

class Cell:
   def __init__(self, x, y):
      self.x = x
      self.y = y


   # Color a cell to surface on grid
   def render(self, surface, grid, color):
      surface.fill(color, grid[self.y][self.x])

   @staticmethod
   def distance(self, other):
      return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
   

   # Bresenham's line drawing algorithm
   @staticmethod
   def render_line(cell_a, cell_b, surface, grid, obs, color):
      dx, dy = cell_a.x - cell_b.x, cell_a.y - cell_b.y
      dx_abs, dy_abs = abs(dx), abs(dy)
      px, py = 2 * dy_abs - dx_abs, 2 * dx_abs - dy_abs

      if dx_abs > dy_abs:
         if dx < 0:
            xs, xe, y = cell_a.x, cell_b.x, cell_a.y
         else:
            xs, xe, y = cell_b.x, cell_a.x, cell_b.y

         while xs <= xe:
            surface.fill(color, grid[y][xs])
            obs[y][xs] = True
            xs += 1
            if px < 0:
               px += 2 * dy_abs
            else:
               y += (1 if dx * dy > 0 else -1) 
               px += 2 * (dy_abs - dx_abs)
      else:
         if dy < 0:
            ys, ye, x = cell_a.y, cell_b.y, cell_a.x
         else:
            ys, ye, x = cell_b.y, cell_a.y, cell_b.x

         while ys <= ye:
            surface.fill(color, grid[ys][x])
            obs[ys][x] = True
            ys += 1
            if py < 0:
               py += 2 * dx_abs
            else:
               x += (1 if dx * dy > 0 else -1)
               py += 2 * (dx_abs - dy_abs)


   # Parse cell from line
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
         raise Exception('MAP: Fail to init cell from line \'{}\'' \
                        .format(line))
         return

      return cells


class Border:
   def __init__(self, w, h):
      self.w = w
      self.h = h
      self.rect = pg.Rect((0, 0, self.w * scale_pxl, self.h * scale_pxl))


   def create_grid(self):
      grid = [[pg.Rect((0, 0, scale_pxl, scale_pxl)) \
               for j in range(self.w)] for i in range(self.h)]
      return grid


   # Draw grid of cells within border
   def render(self, surface, grid, color):
      self.rect.center = surface.get_rect().center
      pg.draw.rect(surface, color, self.rect, 2)

      for i in range(self.h):
         for j in range(self.w):
            grid[i][j].x = self.rect.x + scale_pxl * j
            grid[i][j].y = self.rect.y + scale_pxl * i
            pg.draw.rect(surface, color, grid[i][j], 1)            


   def get_size(self):
      return (0, 0, self.w, self.h)


   # Parse border from line
   @staticmethod
   def init_from(line, delim=','): 
      try:
         w, h = map(int, line.split(delim))
         new_border = Border(w, h)
      except:
         raise Exception('MAP: Fail to init border from line \'{}\'' \
                        .format(line))
         return

      return new_border


class Obstacle:
   def __init__(self, cells):
      self.cells = cells


   def render(self, surface, grid, visited, color):
      len_O = len(self.cells)
      for i in range(len_O + 1):
         Cell.render_line(self.cells[i % len_O], \
                          self.cells[(i + 1) % len_O], \
                          surface, grid, visited, color)


   # Parse obstacle from line
   @staticmethod
   def init_from(line, delim=','):
      try:
         cells = Cell.init_from(line, delim)
         new_obstacle = Obstacle(cells)
      except:
         raise Exception('MAP: Fail to init obstacle from line \'{}\'' \
                         .format(line))
         return
   
      return new_obstacle


class Map:
   def __init__(self):
      self.border = None
      self.S = self.G = None
      self.stops = []
      self.O = []

   # Draw a map, which includes draw grid,
   # start node, end node and obstacles
   def render(self, surface, grid):
      obs = [[False] * len(grid[0]) for _ in range(len(grid))]

      self.border.render(surface, grid, pg.Color('lightsteelblue'))
      self.S.render(surface, grid, pg.Color('steelblue'))
      self.G.render(surface, grid, pg.Color('tomato'))
      for e in self.stops:
         e.render(surface, grid, pg.Color('khaki'))
      for e in self.O:
         e.render(surface, grid, obs, pg.Color('lightgray'))

      return obs

   # Load a map from file
   def load(self, path):
      try:
         map_f = open(path, 'r')
      except:
         raise Exception('MAP: Fail to init map from \'{}\''.format(path))
         return

      try:
         self.border = Border.init_from(map_f.readline().rstrip('\n'))
         self.S, self.G, *self.stops = \
                  tuple(Cell.init_from(map_f.readline().rstrip('\n')))

         len_O = int(map_f.readline().rstrip('\n'))
         for _ in range(len_O):
            self.O.append(Obstacle.init_from(map_f.readline(). \
                                             rstrip('\n')))
      except Exception as e:
         raise Exception('MAP: {}'.format(e))
      
      map_f.close()
      grid = self.border.create_grid()
      print('MAP: Successfully load map from \'{}\''.format(path))
      return self.border.get_size(), grid
