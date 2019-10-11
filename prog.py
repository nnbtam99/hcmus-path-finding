import util
import graph

dlg_input = util.InputDialog(name='World Map', size=(0, 0, 400, 200), \
                             title='Map file:')
state, path = dlg_input.run()
if state == 1:
   print('User enters path:', path)
   world_map = graph.Map(path)

