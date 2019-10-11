import pygame as pg

class Node:
   def __init__(self, x=-1, y=-1):
      self.x = x
      self.y = y

class Polygon:
   def __init__(self, poly_description):
      self.n_nodes = 0
      self.nodes = []
      try:
         print('Trying to parse', poly_description)
         self.parse(poly_description)
         print('Successfully parse', poly_description)
      except:
         raise Exception('Cannot init a polygon')
         return

   def parse(self, d):
      try:
         print('Trying to split')
         coors = list(map(int, d.split(',')))
         print('Successfuly split')
      except:
         raise Exception()

      print('1')
      if len(coors) % 2 != 0:
         print('Violate len')
         raise Exception('Poly description should be multiple of 2')
         return

      print('2')
      self.n_nodes = len(coors) // 2
      print('Parse each coors')
      for i in range(self.n_nodes):
         print(i * 2, i * 2 + 1)
         x, y = coors[i * 2], coors[i * 2 + 1]
         print(4)
         self.nodes.append(Node(x, y))
         print(5)


class Map:
   def __init__(self, path):
      self.w = 0
      self.h = 0
      self.snode = None
      self.gnode = None
      self.n_obstacles = 0
      self.obstacles = []
      try:
         self.load_map(path)
      except:
         raise Exception('Cannot initialize map')
         return

   def load_map(self, path):
      try:
         print('Loading...')
         f = open(path, 'r')
         self.x, self.y = map(int, f.readline().rstrip('\n').split(','))
         sx, sy, gx, gy = map(int, f.readline().rstrip('\n').split(','))
         self.snode = Node(sx, sy)
         self.gnode = Node(gx, gy)
         self.n_obstacles = int(f.readline().rstrip('\n'))
                 
         for i in range(self.n_obstacles):
            new_poly = Polygon(f.readline().rstrip('\n'))
            print('Create new polygon')
            self.obstacles.append(new_poly)
            print('appended')
   
         f.close()
         print('Successfully loading world map')
      except:
         raise Exception()
