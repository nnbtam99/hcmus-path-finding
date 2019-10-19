import sys
sys.path.append('../')
from graph import Cell, Map
from algo.dijkstra import dijkstra_group
from math import exp
import random

# 4 directions
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]
INF = int(1e9)

def sa_tsp(s, f, stops, w, h, obs):
   def distance_matrix(s, f, stops, w, h, obs):
      cities = stops.copy()
      cities.append(s)
      cities.append(f)
      dist = {}

      # Find cost of shortest paths of all pair stops
      for stop in cities:
         dist[stop] = {}
         dijkstra_group(stop, cities, w, h, obs, dist[stop])

      return dist

   def acc_prob(d, T):
      """
      If new solution is better than old solution, accept it (p = 1)
      Else, acceptance probability is 1 / (1 + e^(d / T))
      Note: we accept worse solution to avoid being stuck in local optima
      """
      return 1 if d <= 0 else 1 / (1 + exp(d / T))
   
   def energy(s, f, route, dist):
      # Calculate cost of new schedule
      n_stops  = len(route)
      total    = dist[s][route[0]] + dist[route[n_stops - 1]][f]

      for i in range(n_stops - 1):
         total += dist[route[i]][route[i + 1]]
      return total

   def move(route):
      """
      From current solution, move to neighbor solution
      by swaping random pair of stops
      """

      n_stops     = len(route)
      a, b        = random.randint(0, n_stops - 1), \
                    random.randint(0, n_stops - 1)
      new_route   = route.copy()
      new_route[a], new_route[b] = new_route[b], new_route[a]
      return new_route


   # Init distance matrix
   dist = distance_matrix(s, f, stops, w, h, obs)

   # Init state: shuffle all the stops
   random.shuffle(stops)

   # Assume that the initial set of stops are in optimal order
   prev_route     = stops.copy()
   best_route     = prev_route.copy()
   prev_energy    = best_energy = energy(s, f, prev_route, dist)

   # Annealing parameters
   alpha       = 0.95         # Cooling constant
   T           = 100          # Initial temperature
   T_min       = 1            # Terminate temperature

   # Cooling until temperature < T_min
   while T > T_min:

      # Move to a new random neighbor set of stops
      curr_route     = move(prev_route)
      curr_energy    = energy(s, f, curr_route, dist)

      # Measure new set of stops
      delta          = curr_energy - prev_energy
      P              = acc_prob(delta, T)
      
      # Accept new set of stops with certain probability
      if P >= random.uniform(0, 1):
         prev_route  = curr_route.copy()
         prev_energy = curr_energy
      
      if curr_energy < best_energy:
         best_route  = curr_route.copy()
         best_energy = curr_energy

      # Decrease the annealing temperature
      T  *= 0.95

   # Container
   has_path = True
   best_route.insert(0, s)
   best_route.append(f)

   i = 0
   total = 0
   path = []

   while has_path and i < len(best_route) - 1:
      u, v = best_route[i], best_route[i + 1]
      cost = dist[u]['cost'][v.y][v.x]
      has_path &= (cost != INF)
      
      if has_path:
         path.extend(Map.trace_path_by_dir(u, v, dist[u]['path']))

      total += cost
      i += 1

   return has_path, path
