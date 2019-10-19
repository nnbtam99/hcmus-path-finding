# Import libaries
import pygame as pg
from pygame.locals import *

# Import algorithms
from algo.bfs import bfs
from algo.dfs import dfs
from algo.dijkstra import dijkstra
from algo.greedy_bfs import greedy_bfs
from algo.a_star import a_star
from algo.sa import sa_tsp

# Import extensions
from ext.eztext import Input as TextHolder

font        = pg.font.Font('./static/font/nunito.ttf', 13)
font_bold   = pg.font.Font('./static/font/nunito-bold.ttf', 14)
clock       = pg.time.Clock()
FPS         = 25


class World:

   # Constructor
   def __init__(self, world_map, grid, size):
      self.done         = 0
      self.map          = world_map
      self.size         = size
      self.grid         = grid
      self.algo_names   = []
      self.inp          = None
      self.is_obstacle  = None
      self.surface      = None

   # Draw map on the surface
   def render_map(self, movable=False):
      self.obs          = self.map.render(surface=self.surface, grid=self.grid, movable=movable)

   """
   Display world's components:
   - Grid
   - Algorithms' names
   - Input box
   """
   def display(self):

      # Configure window
      wnd_rect          = pg.Rect(self.size)
      self.surface      = pg.display.set_mode((wnd_rect.w * 30, \
                                               wnd_rect.h * 25))
      self.surface.fill(pg.Color('white'))

      # Render map
      self.render_map()

      # Display algorithm options
      title_text           = 'Algorithms:'
      title_box            = font_bold.render(title_text, True, pg.Color('darkred'))
      title_rect           = title_box.get_rect()
      title_rect.center    = self.surface.get_rect().center
      title_rect.x         = self.map.border.rect.x + self.map.border.rect.w + 50
      title_rect.y         -= 80
      self.surface.blit(title_box, title_rect)

      prev_y               = title_rect.y + 8
      self.algo_names      = ['BFS', 'DFS', 'Dijkstra', \
                              'Greedy BFS', 'A*', \
                              'Simulated Annealing', 'Moving Map']

      for idx, e in enumerate(self.algo_names):
         opt_box           = font.render('{}. {}'.format(idx + 1, e), \
                                         True, pg.Color('darkred'))
         opt_rect          = opt_box.get_rect()
         opt_rect.x        = title_rect.x + 20
         opt_rect.y        = prev_y + title_rect.h
         prev_y            = opt_rect.y
         self.surface.blit(opt_box, opt_rect)      

      # Display input box
      outline_box_size     = (title_rect.x, prev_y + 30, 200, 25)
      outline_box_rect     = pg.Rect(outline_box_size)
      pg.draw.rect(self.surface, pg.Color('darkred'), outline_box_rect, 1)
      
      inp_size = inp_x, inp_y = outline_box_rect.x + 8, \
                                outline_box_rect.y + 5
      self.inp = TextHolder(x=inp_x, y=inp_y, maxlength=1, width=21, \
                            font=font, restricted='1234567', \
                            prompt='> Your choice: ')
      self.inp.draw(self.surface)

      # Update changes
      pg.display.update()


   def display_path(self, has_path, path, color):
      if not has_path:
         print('PATH: No path found')
         return

      print('PATH: Tracing...')

      for e in path:

         # Fill nodes in path
         self.surface.fill(color, self.grid[e.y][e.x])

         # Update changes
         pg.display.update()

         clock.tick(FPS)

      print('PATH: Finish tracing')


   def find_path(self, algo):
      self.render_map()
      has_path, path = False, None

      if algo == 'BFS':
         has_path, path = bfs(self.map.S, self.map.G, self.map.border.w, \
                              self.map.border.h, self.obs)
      elif algo == 'DFS':
         has_path, path = dfs(self.map.S, self.map.G, self.map.border.w, \
                              self.map.border.h, self.obs)
      elif algo == 'Greedy BFS':
         has_path, path = greedy_bfs(self.map.S, self.map.G, \
                           self.map.border.w, self.map.border.h, self.obs)
      elif algo == 'Dijkstra':
         has_path, path = dijkstra(self.map.S, self.map.G, \
                           self.map.border.w, self.map.border.h, self.obs)
      elif algo == 'A*':
         has_path, path = a_star(self.map.S, self.map.G, \
                           self.map.border.w, self.map.border.h, self.obs)
      elif algo == 'Simulated Annealing':
         has_path, path = sa_tsp(self.map.S, self.map.G, self.map.stops, \
                           self.map.border.w, self.map.border.h, self.obs)
      elif algo == 'Moving Map':
         while True:
            self.render_map(movable=True)
            clock.tick(5)
            pg.display.update()


      print('* Running {}:'.format(algo))
      self.display_path(has_path, path, pg.Color('skyblue'))

   def run(self):
      self.display()

      while self.done == 0:
         events = pg.event.get()

         # Update user input
         self.inp.update(events)
         self.surface.fill(pg.Color('white'), self.inp.get_rect())
         self.inp.draw(self.surface)

         for e in events:
            
            # Terminate if user clicks exit button
            if e.type == pg.QUIT:
               self.done = 1
               continue

            # If user hits ENTER
            if e.type == pg.KEYDOWN and e.key == K_RETURN:

               # Get user input
               if self.inp.get_text() != '':

                  # Get index of algorithm to run
                  algo_idx = int(self.inp.get_text())

                  # Run selected algorithm on map
                  self.find_path(self.algo_names[algo_idx - 1])

               self.inp.reset_text()
               self.surface.fill(pg.Color('white'), self.inp.get_rect())
               self.inp.draw(self.surface)

         pg.display.flip()
