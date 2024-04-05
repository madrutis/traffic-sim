import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import IPython.display as display
import random as rand


class Car:
   def __init__(self, lane, position, speed, technique, length=1):
      self.lane = lane
      self.pos = position
      self.speed = speed
      self.length = length

      self.desired_speed = None
      self.accel = None
      self.assign_characteristics(technique)
      
   
   def assign_characteristics(self, technique):
      if technique == "Reckless":
         pass
      elif technique == "Cautious":
         pass
      else:
         pass


class Simulation:
   def __init__(self, num_cars, tecnhique_distrib, num_lanes=3, lane_length=100):
      self.num_lanes = num_lanes
      self.num_cars = num_cars
      self.cars = []
      self.lanes = [[] for _ in range(num_lanes)]
      cars_per_lane = num_cars // num_lanes
      extra_cars = num_cars % num_lanes
      

      car_tecniques = np.random.choice(["Reckless", "Cautious", "Normal"], num_cars, p=tecnhique_distrib)
      for lane in range(num_lanes):
         for i in range


      
      




if __name__ == "__main__":
   pass 