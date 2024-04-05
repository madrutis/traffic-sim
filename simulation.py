import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import IPython.display as display
import random as rand


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
      cars_per_lane = num_cars // num_lanes
      # cars that don't evenly fit in the lanes
      extra_cars = num_cars % num_lanes

      # add extra cars to the last lane
      lane_capacity = [cars_per_lane for _ in num_lanes]
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
      
   def plot_starting_conditions(self):
      positions = [[] for _ in self.num_lanes]
      for lane_num, lane in enumerate(self.lanes):
         for car in lane:
            positions[lane_num].append((car.back + car.front) / 2)
      
      plt.figure(figsize=(10, 6))  # Adjust figure size if needed

      # Plot road lines for each lane
      plt.plot([0, 15], [0.1, 0.1], color='gray', linestyle='--', linewidth=1)  # Lane 1
      plt.plot([0, 15], [0.2, 0.2], color='gray', linestyle='--', linewidth=1)  # Lane 2
      plt.plot([0, 15], [0.3, 0.3], color='gray', linestyle='--', linewidth=1)  # Lane 3

      # Plot cars
      plt.scatter(positions[0], [0.1]*len(positions[0]), color='red', label='Lane 1')
      plt.scatter(positions[1], [0.2]*len(positions[1]), color='blue', label='Lane 2')
      plt.scatter(positions[2], [0.3]*len(positions[2]), color='green', label='Lane 3')

      # Customize plot
      plt.xlabel('Position')
      plt.ylabel('Lane')
      plt.title('Car Positions Along Three Lanes')
      plt.yticks([0.1, 0.2, 0.3], ['Lane 1', 'Lane 2', 'Lane 3'])
      plt.grid(True)
      plt.legend()

      # Show plot
      plt.tight_layout()
      plt.show()




      


if __name__ == "__main__":
   highway_sim = Simulation(30, 1, [1, 0, 0], 3, 100)
   highway_sim.plot_starting_conditions()
