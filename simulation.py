import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import IPython.display as display
import random as rand
from pprint import pprint


class Car:
   def __init__(self, lane, back, front, speed, technique, length=1):
      self.lane = lane
      self.speed = speed
      self.length = length
      self.front = front
      self.back = back

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
   def __init__(self, num_cars, car_length, tecnhique_distrib, num_lanes=3, lane_length=100):
      self.num_lanes = num_lanes
      self.num_cars = num_cars
      self.cars = []
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
         empty_space = lane_length - car_length * num_cars
         space_between_car = empty_space / num_cars
         speed = 0
         position = 0
         for car in range(cars_per_lane):
            new_car = Car(lane, position, position + car_length, speed, car_techniques[car_index], car_length)
            self.lanes[lane].append(new_car)
            car_index += 1
            position += car_length + space_between_car
      
   def plot_starting_conditions(self):
      positions = [[] for _ in range(self.num_lanes)]
      for lane_num, lane in enumerate(self.lanes):
         for car in lane:
            positions[lane_num].append((car.back + car.front) / 2)
      
      
      pprint(positions)
      plt.figure(figsize=(10, 6))  # Adjust figure size if needed

      # Plot road lines for each lane
      for lane in range(self.num_lanes):
         plt.plot([0, self.lane_length], [lane * .05, lane * .05], color='gray', linestyle='--', linewidth=1)

      # Plot cars
      for lane in range(self.num_lanes):
         plt.scatter(positions[lane], [lane * .05]*len(positions[lane]), label=f'Lane {lane}')
      # Customize plot
      plt.xlabel('Position')
      plt.ylabel('Lane')
      plt.title('Car Positions Along Three Lanes')
      plt.yticks([lane * .05 for lane in range(self.num_lanes)], [f"Lane{lane}" for lane in range(self.num_lanes)])
      plt.legend()

      # Show plot
      plt.tight_layout()
      plt.show()
      plt.savefig('starting_conditions.png')




      


if __name__ == "__main__":
   highway_sim = Simulation(30, 1, [1, 0, 0], 3, 100)
   highway_sim.plot_starting_conditions()
