import sys
sys.path.append('../')
from graph import Cell, Map
from algo.dijkstra import dijkstra_net
from math import exp
import random

INF = int(1e9)

def sa_tsp(s, f, stops, w, h, restricted):

   def distance_matrix():
      cities         = stops.copy()
      cities.append(s)
      cities.append(f)
      dist           = {}
      
      # Find cost of shortest paths between all pair of stops
      for each in cities:
         dist[each]  = {}
         dijkstra_net(s=each, fs=cities, w=w, h=h, \
                      restricted=restricted, container=dist[each])
      
      return dist

   def acc_prob(d, T):
      """
      If new solution is better than old solution, accept it (p = 1)
      Else, acceptance probability using Boltzman prob is e^(-d / T))
      Note: we accept worse solution to avoid being stuck in local optima
      """
      return 1 if d <= 0 else exp(-d / T)
   
   def energy(route):
      cities = route.copy()
      cities.insert(0, s)
      cities.append(f)
     
      # Calculate cost of new schedule
      n_stops  = len(cities)
      total    = 0

      for i in range(n_stops - 1):
         total += dist[cities[i]][cities[i + 1]]

      return total

   def move(route):
      """
      From current solution, move to neighbor solution
      by swaping random pair of stops
      """

      n_stops     = len(route)
      if n_stops == 0:
         return
      
      a, b        = random.randint(0, n_stops - 1), \
                    random.randint(0, n_stops - 1)
      new_route   = route.copy()
      new_route[a], new_route[b] = new_route[b], new_route[a]
      return new_route

   # Calculate distance matrix
   dist           = distance_matrix()
   has_path       = True
   path           = []
   total          = 0

   if len(stops) == 0:
      total       = dist[s][f]
      has_path    &= (total != INF)
      
      if has_path:
         path.extend(Map.trace_path_by_dir(s=s, f=f, dirs=dist[s]['dirs']))

   else:

      # Initial solution
      random.shuffle(stops)

      prev_route     = stops.copy()
      best_route     = prev_route.copy()
      prev_energy    = best_energy = energy(prev_route)

      # Annealing parameters
      alpha          = 0.95                        # Cooling constant
      T              = (w + h) * (w + h - 1) / 2   # Initial temperature
      T_min          = 1                           # Terminate temperature

      # Cooling until temperature < T_min
      while T > T_min:

         # Create a random neighbor solution
         curr_route     = move(prev_route)
         curr_energy    = energy(curr_route)

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
         T  *= alpha

      
      best_route.insert(0, s)
      best_route.append(f)

      i = 0
      
      while has_path and i < len(best_route) - 1:
         u, v           = best_route[i], best_route[i + 1]
         cost           = dist[u][v]
         has_path       &= (cost != INF)
      
         if has_path:
            path.extend(Map.trace_path_by_dir(s=u, f=v, dirs=dist[u]['dirs']))

         total += cost
         i += 1

   return has_path, total, path
