import pygame as pg
import pygame.gfxdraw as pxl
from pygame.locals import *
from ext.eztext import Input as TextHolder

pg.init()
pg.font.init()

default_title_font = pg.font.Font('./static/font/nunito.ttf', 13)
default_input_font = pg.font.Font('./static/font/nunito.ttf', 14)

class InputDialog:
   def __init__(self, name, size, title, \
                title_font=default_title_font, \
                input_font=default_input_font):
      try:
         self.done = 0
         self.name = name
         self.size = size
         self.title = title
         self.inp = None
         self.surface = None
         self.render(title_font, input_font)
      except Exception as e:
         raise(Exception(str(e)))
         return

   def render(self, title_font, input_font):
      pg.display.set_caption(self.name)

      # Draw dialog      
      dialog_rect = pg.Rect(self.size)
      self.surface = pg.display.set_mode((dialog_rect.w, dialog_rect.h))
      self.surface.fill(pg.Color('white'))

      # Draw box outline
      outline_box_size = (0, 0, dialog_rect.w * 0.6, dialog_rect.h * 0.2)
      outline_box_rect = pg.Rect(outline_box_size)
      outline_box_rect.center = dialog_rect.center
      pg.draw.rect(self.surface, pg.Color('lavender'), \
                   outline_box_rect, 1)

      # Draw title
      title_box = title_font.render(self.title, False, pg.Color('black'))
      title_rect = title_box.get_rect()
      title_rect.x = outline_box_rect.x + 8
      title_rect.y = outline_box_rect.y - 22
      self.surface.blit(title_box, title_rect)

      # Draw input box
      inp_size = inp_x, inp_y = outline_box_rect.x + 8, \
                                outline_box_rect.y + 15
      self.inp = TextHolder(x=inp_x, y=inp_y, maxlength=23, \
                            font=input_font, prompt='> ')
      self.inp.draw(self.surface)
      
      pg.display.update()
      


   def run(self):
      while self.done == 0:
         events = pg.event.get()
         self.inp.update(events)
         self.surface.fill(pg.Color('white'), self.inp.get_rect())
         self.inp.draw(self.surface)

         for e in events:
            if e.type == pg.QUIT:
               self.done = -1
            elif e.type == pg.KEYDOWN and e.key == K_RETURN:
               self.done = 1
         pg.display.flip()

      return (1, self.inp.get_text()) if self.done == 1 else \
             (-1, None)
