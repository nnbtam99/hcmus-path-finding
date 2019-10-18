import sys
sys.path.append('../')
from graph import Cell
from math import exp
import random

# 8 directions
dx = [0, 0, 1, -1, 1, 1, -1, -1]
dy = [1, -1, 0, 0, 1, -1, 1, -1]

def sa_tsp(s, f, w, h, obs, stops):
   def acc_prob(d, T):
      return 1 if d <= 0 else 1 / (1 + exp(d / T))
   
   def energy(route, s, f):
      n_stops  = len(route)
      total    = Cell.distance(s, route[0]) + \
                 Cell.distance(route[n_stops - 1], f)

      for i in range(n_stops - 1):
         total += Cell.distance(route[i], route[i + 1])
      return total

   def move(route):
      n_stops     = len(route)
      a, b        = random.randint(0, n_stops - 1), \
                    random.randint(0, n_stops - 1)
      new_route   = route.copy()
      new_route[a], new_route[b] = new_route[b], new_route[a]
      return new_route

   # Shuffle all the stops
   random.shuffle(stops)

   # Assume that the initial set of stops are optimal
   prev_route     = stops.copy()
   best_route     = prev_route.copy()
   prev_energy    = best_energy = energy(prev_route, s, f)

   # Annealing parameters
   alpha       = 0.95         # Cooling constant
   T           = 100          # Initial temperature
   T_min       = 1            # Terminate temperature

   # Cooling until temperature reaches T_in
   while T > T_min:

      # Move to a new random neighbor set of stops
      curr_route     = move(prev_route)
      curr_energy    = energy(curr_route, s, f)

      # Measure new set of stops
      delta          = curr_energy - prev_energy
      P              = acc_prob(delta, T)
      print('Prob:', P)

      """
      Accept new set of stops with certain probability
      If the current schedule is better, set it as the best
      Else, accept worse schedule with acceptance probability
      To avoid standing in the local optima
      """
      if P >= random.uniform(0, 1):
         prev_route  = curr_route.copy()
         prev_energy = curr_energy
      
      if curr_energy < best_energy:
         best_route  = curr_route.copy()
         best_energy = curr_energy

      # Decrease the temperature
      T  *= 0.95

   for e in best_route:
      print(e.x, e.y)




