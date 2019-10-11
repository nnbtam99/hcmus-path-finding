import pygame as pg
from pygame.locals import *
import sys
from mainscreen import Map
from lib import eztext

pg.init()
pg.font.init()

class Screen01:
   def __init__(self, name):
      self.done = False
      self.screen = None
      self.box_rect = None
      self.box_input = None
      self.name = name
      self.clock = pg.time.Clock()

   def display(self):
      pg.display.set_caption('World Map')
      title_font = pg.font.Font('./static/font/nunito.ttf', 11)
      input_font = pg.font.Font('./static/font/nunito.ttf', 13)

      # Configure window
      window_size = (0, 0, 400, 200)
      window_rect = pg.Rect(window_size)
      self.screen = pg.display.set_mode((window_rect.w, window_rect.h))
      self.screen.fill(pg.Color('white'))
   
      # Configure box outlier
      box_outlier_size = (0, 0, 175, 25)
      box_outlier_rect = pg.Rect(box_outlier_size)
      box_outlier_rect.center = window_rect.center
      pg.draw.rect(self.screen, pg.Color('lavender'), box_outlier_rect, 1)

      # Configure box input
      box_size = (0, 0, box_outlier_rect.w - 5, box_outlier_rect.h - 5)
      self.box_rect = pg.Rect(box_size)
      self.box_rect.center = window_rect.center

      # Configure box title
      text_title = title_font.render('Map file:', False, pg.Color('black'))
      text_rect = text_title.get_rect()
      text_rect.center = window_rect.center
      text_rect.x = self.box_rect.x
      text_rect.y = self.box_rect.y - 20
      self.screen.blit(text_title, text_rect)

      # Configure text input
      self.box_input = eztext.Input(x=self.box_rect.x + 5, y=self.box_rect.y + 2, \
                                    maxlength=22, font=input_font, prompt='> ')
      self.box_input.draw(self.screen)
      pg.display.update()
   
   def redraw_box_rect(self):
      self.screen.fill(pg.Color('white'), self.box_rect)

   def start(self):
      self.display()
      world_map = None

      while not self.done:
         self.clock.tick(30)
         events = pg.event.get()
         for event in events:
            if event.type == pg.QUIT:
               self.done = True
               continue
            elif event.type == pg.KEYDOWN and event.key == K_RETURN:
               try:
                  world_map = Map(self.box_input.get_text())
                  self.done = True
                  continue
               except Exception as error:
                  print(str(error))

         self.redraw_box_rect()
         self.box_input.update(events)
         self.box_input.draw(self.screen)
         pg.display.flip()

      return world_map
