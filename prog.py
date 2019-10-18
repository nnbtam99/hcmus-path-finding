import util
import graph
import world
import pygame as pg

# FPS = 20
dlg_input = util.InputDialog(name='World Map', size=(0, 0, 400, 200), \
                             title='Map file:')
state, path = dlg_input.run()

# clock = pg.time.Clock()

if state == 1:
   # clock.tick(FPS)
   print('User enters path:', path)
   try:
      world_map = graph.Map()
      world_size, world_grid = world_map.load(path)
      world = world.World(world_map, world_grid, world_size)
      world.run()

   except Exception as e:
      print(str(e))
      exit()
elif state == -1:
   exit()
