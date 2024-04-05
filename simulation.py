import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import IPython.display as display
import random as rand
from pprint import pprint
import time

#%matplotlib

class Car:
   reckless = {"desired_speed": 1.5, "accel": .2, "decel": .5}
   cautious = {"desired_speed": .9, "accel": .05, "decel": .3}
   normal = {"desired_speed": 1, "accel": .1, "decel": .4}

   def __init__(self, lane, position, speed, technique, length=1):
      self.lane = lane
      self.speed = speed
      self.length = length
      self.pos = position

      self.desired_speed = None
      self.desire_accel = None
      self.desired_decel = None
      self.accel = None
      self.decel = None
      self.assign_characteristics(technique)
      
   
   def assign_characteristics(self, technique):
      if technique == "Reckless":
         self.assign_metrics(Car.reckless)
      elif technique == "Cautious":
         self.assign_metrics(Car.cautious)
      else:
         self.assign_metrics(Car.normal)
   
   def assign_metrics(self, technique):
      self.desired_speed = np.random.normal(technique["desired_speed"], 0.1)
      self.desired_accel = np.random.normal(technique["accel"], .02)
      self.desired_decel = np.random.normal(technique["decel"], .02)
      self.accel = self.desired_accel
      self.decel = self.desired_decel
   
   def check_bounds(self, lane_length):
      if self.pos >= lane_length:
         self.pos = self.pos % lane_length



class Simulation:
   def __init__(self, num_cars, car_length, tecnhique_distrib, num_lanes=3, lane_length=100):
      self.num_lanes = num_lanes
      self.num_cars = num_cars
      self.cars = {}
      self.lanes = [[] for _ in range(num_lanes)]
      
      self.lane_length = lane_length
      cars_per_lane = num_cars // num_lanes
      # cars that don't evenly fit in the lanes
      extra_cars = num_cars % num_lanes

      # add extra cars to the last lane
      lane_capacity = [cars_per_lane for _ in range(num_lanes)]
      lane_capacity[-1] += extra_cars

      car_techniques = np.random.choice(["Reckless", "Cautious", "Normal"], num_cars, p=tecnhique_distrib)

      car_index = 0
      for lane, cars_per_lane in enumerate(lane_capacity):
         empty_space = lane_length - car_length * cars_per_lane
         space_between_car = empty_space / cars_per_lane
         speed = 0
         position = 0
         for car in range(cars_per_lane):
            new_car = Car(lane, position, speed, car_techniques[car_index], car_length)
            self.cars[car_index] = new_car
            self.lanes[lane].append(car_index)
            car_index += 1
            position += car_length + space_between_car
      
   def plot(self):
      positions = [[] for _ in range(self.num_lanes)]
      for lane_num, lane in enumerate(self.lanes):
         for car_index in lane:
            positions[lane_num].append(self.cars[car_index].pos)
      
      plt.figure(figsize=(10, 3))  # Adjust figure size if needed

      # Plot road lines for each lane
      for lane in range(self.num_lanes):
         plt.plot([0, self.lane_length], [lane * .05, lane * .05], color='gray', linestyle='--', linewidth=1)

      # Plot cars
      for lane in range(self.num_lanes):
         plt.scatter(positions[lane], [lane * .05]*len(positions[lane]), label=f'Lane {lane}')
      # Customize plot
      plt.xlabel('Position')
      plt.ylabel('Lane')
      plt.title(f'{self.num_lanes} Lane Highway with {self.num_cars} Cars')
      plt.yticks([lane * .05 for lane in range(self.num_lanes)], [f"Lane{lane}" for lane in range(self.num_lanes)])


      # Show plot
      plt.tight_layout()
      print(plt.use('Agg'))
      ax = plt.gca()
      plt.show()
      display.clear_output(wait=True)
      

   def update(self):
      """"Update the simulation by one time step"""
      update_order = np.random.permutation(np.arange(self.num_cars))

      for i in update_order:
         car = self.cars[i]
         car.pos += car.speed
         if car.speed >= car.desired_speed:
            car.accel = 0
         car.speed += car.accel
         car.check_bounds(self.lane_length)

   def run(self, num_steps, plot=True):
      for _ in range(num_steps):
         self.update()
         if plot:
            self.plot()
         time.sleep(0.1)
      



if __name__ == "__main__":
   highway_sim = Simulation(30, 1, [1, 0, 0], 3, 100)
   highway_sim.run(1000)
   
   


