import util
import graph
import world

dlg_input = util.InputDialog(name='World Map', size=(0, 0, 400, 200), \
                             title='Map file:')
state, path = dlg_input.run()
if state == 1:
   print('User enters path:', path)
   try:
      world_map = graph.Map()
      world_size = world_map.load(path)
      world = world.World(world_map, world_size)
      world.display()

   except Exception as e:
      print(str(e))
      exit()
elif state == -1:
   exit()
