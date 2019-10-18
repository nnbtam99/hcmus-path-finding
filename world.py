import pygame as pg
from pygame.locals import *
from algo.bfs import bfs
from algo.dfs import dfs
from algo.dijkstra import dijkstra
from algo.greedy_bfs import greedy_bfs
from algo.a_star import a_star
from algo.sa import sa_tsp
from ext.eztext import Input as TextHolder

font = pg.font.Font('./static/font/nunito.ttf', 13)
font_bold = pg.font.Font('./static/font/nunito-bold.ttf', 14)

class World:
   def __init__(self, world_map, grid, size):
      self.done      = 0
      self.map       = world_map
      self.size      = size
      self.grid      = grid
      self.inp       = None
      self.obs       = None
      self.surface   = None

   def display(self):

      # Configure window
      wnd_rect       = pg.Rect(self.size)
      self.surface   = pg.display.set_mode((wnd_rect.w * 30, \
                                            wnd_rect.h * 25))
      self.surface.fill(pg.Color('white'))

      # Render map and get a trace array of obstacles
      self.obs       = self.map.render(self.surface, self.grid)

      # Display algorithm options
      title_text           = 'Algorithms:'
      title_box            = font_bold.render(title_text, True, \
                                              pg.Color('darkred'))
      title_rect           = title_box.get_rect()
      title_rect.center    = self.surface.get_rect().center
      title_rect.x         = self.map.border.rect.x + \
                             self.map.border.rect.w + 50
      title_rect.y         -= 80
      self.surface.blit(title_box, title_rect)

      prev_y               = title_rect.y + 8
      opt_text_lst         = ['1. BFS', '2. DFS', '3. Dijkstra', \
                              '4. Greedy BFS', '5. A*', \
                              '6. Simulated Annealing']

      for e in opt_text_lst:
         opt_box           = font.render(e, True, pg.Color('darkred'))
         opt_rect          = opt_box.get_rect()
         opt_rect.x        = title_rect.x + 20
         opt_rect.y        = prev_y + title_rect.h
         prev_y            = opt_rect.y
         self.surface.blit(opt_box, opt_rect)      

      outline_box_size = (title_rect.x, prev_y + 30, 200, 25)
      outline_box_rect = pg.Rect(outline_box_size)
      pg.draw.rect(self.surface, pg.Color('darkred'), outline_box_rect, 1)
      
      inp_size = inp_x, inp_y = outline_box_rect.x + 8, \
                                outline_box_rect.y + 5
      self.inp = TextHolder(x=inp_x, y=inp_y, maxlength=1, width=21, \
                            font=font, restricted='123456', \
                            prompt='> Your choice: ')
      self.inp.draw(self.surface)

      # Update changes
      pg.display.update()

   def trace_path(self, has_path, path, color):
      if not has_path:
         print('PATH: No path found')
         return

      print('PATH: Tracing...')

      # Must be consistent with ones used in algorithms
      dx = [0, 0, 1, -1]
      dy = [1, -1, 0, 0]

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

      print('PATH: Finish tracing')


   def find_path(self, algo):
      has_path, path = False, None

      if algo == 'BFS':
         has_path, path = bfs(self.map.S, self.map.G, self.map.border.w, \
                              self.map.border.h, self.obs)
      elif algo == 'DFS':
         has_path, path = dfs(self.map.S, self.map.G, self.map.border.w, \
                              self.map.border.h, self.obs)
      elif algo == 'GreedyBFS':
         has_path, path = greedy_bfs(self.map.S, self.map.G, \
                           self.map.border.w, self.map.border.h, self.obs)
      elif algo == 'Dijkstra':
         has_path, path = dijkstra(self.map.S, self.map.G, \
                           self.map.border.w, self.map.border.h, self.obs)
      elif algo == 'AStar':
         has_path, path = a_star(self.map.S, self.map.G, \
                           self.map.border.w, self.map.border.h, self.obs)

      self.trace_path(has_path, path, pg.Color('skyblue'))

   def run(self):
      self.display()
      self.find_path('DFS')

      while self.done == 0:
         events = pg.event.get()
         self.inp.update(events)
         self.surface.fill(pg.Color('white'), self.inp.get_rect())
         self.inp.draw(self.surface)
         for e in events:
            if e.type == pg.QUIT:
               self.done = 1
               continue

         pg.display.flip()
