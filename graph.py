# Import libraries
from math import ceil
import pygame as pg
from collections import deque

# Global constant
scale_pxl = 15          # Cell's w = h = scale_pxl (scale pixel)

class Cell:

   # Constructor
   def __init__(self, x, y):
      self.x   = x
      self.y   = y 

   # Comparator
   def __lt__(self, other):
      return ((self.x, self.y) < (other.x, other.y))

   @staticmethod
   def distance(first, second):
      dx, dy   = abs(first.x - second.x), abs(first.y - second.y)
      return (dx ** 2 + dy ** 2) ** 0.5
   

   # Draw a cell on the surface with specified color
   def render(self, surface, grid, color):
      surface.fill(color, grid[self.y][self.x])

   """
   Draw line between two cells by Bresenham's line drawing algorithm
   Mark a cell as True if should_mark = True
   """
   @staticmethod
   def render_line(first, second, surface, grid, color, mark=None):
      dx, dy            = first.x - second.x, first.y - second.y
      dx_abs, dy_abs    = abs(dx), abs(dy)
      px, py            = 2 * dy_abs - dx_abs, 2 * dx_abs - dy_abs

      # X-axis dominates
      if dx_abs > dy_abs:
         if dx < 0:
            xs, xe, y   = first.x, second.x, first.y
         else:
            xs, xe, y   = second.x, first.x, second.y

         while xs <= xe:

            # Color cells on line
            surface.fill(color, grid[y][xs])

            # Mark cells on line
            if mark is not None:
               mark[y][xs] = True

            xs          += 1
            if px < 0:
               px       += 2 * dy_abs
            else:
               y        += (1 if dx * dy > 0 else -1) 
               px       += 2 * (dy_abs - dx_abs)

      # Y-axis dominates
      else:
         if dy < 0:
            ys, ye, x   = first.y, second.y, first.x
         else:
            ys, ye, x   = second.y, first.y, second.x

         while ys <= ye:
            surface.fill(color, grid[ys][x])

            if mark is not None:
               mark[ys][x] = True

            ys          += 1
            if py < 0:
               py       += 2 * dx_abs
            else:
               x        += (1 if dx * dy > 0 else -1)
               py       += 2 * (dx_abs - dy_abs)


   """
   Parse a group of cells from line
   Consider ',' as default delimiter
   """
   @staticmethod
   def init_from(line, delim=','):
      parsed            = []
      try:
         # Split line to integer (coordinates) arrays seperated by delimiter
         list_coors     = list(map(int, line.split(delim)))

         """
         Assump that we're working on 2D coordinate systems,
         Number of parsed coordinates = ceil(number of parsed integers / 2)
         """
         len_coors      = int(ceil(len(list_coors) / 2))

         # Group every 2 coordinates as a cell (x, y)
         for i in range(len_coors):
            x, y        = list_coors[i * 2], list_coors[i * 2 + 1]
            parsed.append(Cell(x=x, y=y))

      except:
         raise Exception('MAP: Fail to init cell from line \'{}\'' \
                        .format(line))
         return

      return parsed


class Border:

   # Constructor
   def __init__(self, w, h):
      self.w      = w
      self.h      = h

      """
      pygame's rectangle, square (to be exactly) object of border on surface
      1 unit of width = a certain number of pixels
      """
      self.rect   = pg.Rect((0, 0, self.w * scale_pxl, self.h * scale_pxl))

   """
   Create a 2D array of square objects
   Each object corresponds to a cell within border on the surface
   """
   def create_grid(self):
      grid        = [[pg.Rect((0, 0, scale_pxl, scale_pxl)) \
                      for j in range(self.w)] for i in range(self.h)]
      return grid


   # Draw grid of cells within border
   def render(self, surface, grid, color):

      # Border's y = surface's y
      self.rect.center  = surface.get_rect().center

      # 10% distance from surface's left edge
      self.rect.x       = surface.get_rect().w * 0.1

      # Draw border with certain color and width = 2
      pg.draw.rect(surface, color, self.rect, 2)

      # Draw cells
      for i in range(self.h):
         for j in range(self.w):
            grid[i][j].x   = self.rect.x + scale_pxl * j
            grid[i][j].y   = self.rect.y + scale_pxl * i

            # Fill cell inside by white color
            surface.fill(pg.Color('white'), grid[i][j])

            # Draw cell outline by color, width = 1
            pg.draw.rect(surface, color, grid[i][j], 1)            


   # Get size of border
   def get_size(self):
      return (0, 0, self.w, self.h)


   """
   Parse border formated as w,h from line
   Consider ',' as default delimiter
   """
   @staticmethod
   def init_from(line, delim=','): 
      try:
         w, h        = map(int, line.split(delim))
         parsed      = Border(w=w, h=h)
      except:
         raise Exception('MAP: Fail to init border from line \'{}\'' \
                        .format(line))
         return

      return parsed

# Create a moving cycle within d units
def moving_steps(d, steps):
   for i in range(d + 1):
      steps.append(i)
   for i in range(d, -d, -1):
      steps.append(i)
   for i in range(-d, 0):
      steps.append(i)
   return steps


class CellObstacle(Cell):
   def __init__(self, x, y, dx=0, dy=0):
      Cell.__init__(self, x, y)

      """
      Queues to generate next coordinates if a cell is moving
      First value corresponds to the delta of x and y of a cell's next state
      """
      self.origin_x  = x
      self.origin_y  = y
      self.next_x    = deque()
      self.next_y    = deque()

      # dx: [0, 1, 2, 3, ..., dx, -dx, -(dx + 1), ..., -3, -2, -1]
      moving_steps(dx, self.next_x)
      moving_steps(dy, self.next_y)


   # Move to next state
   def move(self):
      dx, dy      = self.next_x.popleft(), self.next_y.popleft()
      self.x      = self.origin_x + dx
      self.y      = self.origin_y + dy
      self.next_x.append(dx)
      self.next_y.append(dy)


   """
   Parse a group of obstacles' cells from line
   Consider ',' as default delimiter
   Set moving directions of cells with dx, dy
   """
   @staticmethod
   def init_from(line, dx=0, dy=0, delim=','):
      parsed            = []
      
      try:
         list_coors     = list(map(int, line.split(delim)))
         len_coors      = int(ceil(len(list_coors) / 2))
      
         for i in range(len_coors):
            x, y        = list_coors[i * 2], list_coors[i * 2 + 1]
            parsed.append(CellObstacle(x=x, y=y, dx=dx, dy=dy))
  
      except:
         raise Exception('MAP: Fail to init obstacle cell from line \'{}\'' \
                        .format(line))
         return

      return parsed


class Obstacle:

   # Constructor
   def __init__(self, list_cells):
      self.list_cells   = list_cells

   """
   Each obstacle is defined by a set of vertices
   For each consecutive pair of vertices, draw a line between them on the surface
   Mark and set moving distances to each cells of the obstacle
   """
   def render(self, surface, grid, mark, color, movable=False):
      len_cells         = len(self.list_cells)

      if movable:
         # Update a new state of obstacle of movable = True
         for i in range(len_cells):
            self.list_cells[i].move()
            
      # Draw all pair line betweens consecutive vertices
      for i in range(len_cells + 1):
         u, v           = i % len_cells, (i + 1) % len_cells
         CellObstacle.render_line(first=self.list_cells[u], second=self.list_cells[v], \
                                  surface=surface, grid=grid, mark=mark, color=color)

   """
   Parse a set of coordinates, which define a obstacle, from line
   Consider ',' as default delimiter
   For each obstacle, set a random moving distance
   """
   @staticmethod
   def init_from(line, delim=',', dx=0, dy=0):
      try:
         list_cells     = CellObstacle.init_from(line=line, delim=delim, \
                                                 dx=dx, dy=dy)
         parsed         = Obstacle(list_cells=list_cells)

      except:
         raise Exception('MAP: Fail to init obstacle from line \'{}\'' \
                         .format(line))
         return
   
      return parsed


class Map:

   # Constructor
   def __init__(self):
      self.border = None
      self.S = self.G = None
      self.stops = []
      self.obstacles = []

   """
   Draw map's components: start node, end node, obstacles and border
   Set movable attribute to obstacles
   """
   def render(self, surface, grid, movable=False):
      w, h           = self.border.w, self.border.h
      is_obstacle    = [[False] * w for _ in range(h)]

      self.border.render(surface=surface, grid=grid, color=pg.Color('lightsteelblue'))
      self.S.render(surface=surface, grid=grid, color=pg.Color('steelblue'))
      self.G.render(surface=surface, grid=grid, color=pg.Color('tomato'))

      for e in self.stops:
         e.render(surface=surface, grid=grid, color=pg.Color('khaki'))

      for e in self.obstacles:
         e.render(surface=surface, grid=grid, color=pg.Color('lightgray'), \
                  mark=is_obstacle, movable=movable)

      return is_obstacle
   
   """
   Create a complete path by tracing by directions (N, E, W, S)
   from end node to start node
   """
   @staticmethod
   def trace_path_by_dir(s, f, dirs):
      sx, sy      = s.x, s.y
      fx, fy      = f.x, f.y
      dx          = [0, 0, 1, -1]
      dy          = [1, -1, 0, 0]
      path        = []
      
      """
      Started from end node, continue tracing path 
      until we meet the start node
      """
      while not (fx == sx and fy == sy):

         # Get the direction of parent node
         i        = dirs[fy][fx]

         # Go to parent node of current f
         fx, fy   = fx - dx[i], fy - dy[i]

         # Stop as soon as start node is reached
         if fx == sx and fy == sy:
            break

         path.append(Cell(x=fx, y=fy))

      # Reverse the path from start node to end node
      path.reverse()
      return path


   # Load a map from file
   def load(self, path):
      try:
         map_file       = open(path, 'r')
      except:
         raise Exception('MAP: Fail to init map from \'{}\''.format(path))
         return

      try:
         self.border    = Border.init_from(line=map_file.readline().rstrip('\n'))
         self.S, self.G, *self.stops = \
                           tuple(Cell.init_from(line=map_file.readline().rstrip('\n')))
         len_obstacles  = int(map_file.readline().rstrip('\n'))
         dx = 0
         dy = 1 - dx

         for _ in range(len_obstacles):
            self.obstacles.append(Obstacle.init_from(line=map_file.readline(). \
                          rstrip('\n'), dx=dx, dy=dy))
            dx          = 1 - dx
            dy          = 1 - dx

      except Exception as e:
         raise Exception('MAP: {}'.format(e))
      
      map_file.close()
      grid = self.border.create_grid()

      print('MAP: Successfully load map from \'{}\''.format(path))
      return self.border.get_size(), grid
