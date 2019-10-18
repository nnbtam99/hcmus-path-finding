import os
import util
import graph
import world

# Center pygame window
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Pop-up to get file path
dlg_input = util.InputDialog(name='World Map', size=(0, 0, 400, 200), \
                             title='Map file:')
state, path = dlg_input.run()

# Check if user entered the path
if state == 1:
   print('User enters path:', path)
   try:
      world_map = graph.Map()
      world_size, world_grid = world_map.load(path)
      world = world.World(world_map, world_grid, world_size)
      world.run()

   except Exception as e:
      print(str(e))
      exit()

# Exit if user clicked exit button
elif state == -1:
   exit()
