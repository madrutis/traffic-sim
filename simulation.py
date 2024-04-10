import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import IPython.display as display
import random as rand
from pprint import pprint
import time

#%matplotlib

class Car:
   reckless = {"desired_speed": 1.5, "accel": .2, "decel": .7, "threshold": 10, "patience": 5}
   cautious = {"desired_speed": .9, "accel": .03, "decel": .3, "threshold": 30, "patience": 12}
   normal = {"desired_speed": 1, "accel": .1, "decel": .4, "threshold": 18, "patience": 8}

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
      self.technique = technique
      self.waiting_for = 0

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
      self.desired_accel = np.random.normal(technique["accel"], .01)
      self.desired_decel = np.random.normal(technique["decel"], .01)
      self.accel = self.desired_accel
      self.decel = self.desired_decel
      self.threshold = technique["threshold"]
      self.patience = technique["patience"]
   
   def check_bounds(self, lane_length):
      if self.pos >= lane_length:
         self.pos = self.pos % lane_length

   def distance_to_car(self, car, lane_length):
      # make sure that this accounts for the looping nature of the road
      return min(car.pos - self.pos, lane_length + car.pos - self.pos)



class Simulation:
   def __init__(self, num_cars, car_length, tecnhique_distrib, num_lanes=3, lane_length=100):
      self.frames = None
      self.num_lanes = num_lanes
      self.num_cars = num_cars
      self.cars = {}
      self.lanes = [[] for _ in range(num_lanes)]
      self.driving_type_colors = {
         'Reckless': 'red',
         'Normal': 'blue',
         'Cautious': 'green'
      }

      self.num_cars_by_technique = {"Reckless": 0, "Cautious": 0, "Normal": 0}

      self.num_waiting_per_timestep = []
      self.num_waiting_by_tecnique = {"Reckless": [], "Cautious": [], "Normal": []}

      self.lane_length = lane_length
      cars_per_lane = num_cars // num_lanes
      # cars that don't evenly fit in the lanes
      extra_cars = num_cars % num_lanes

      # add extra cars to the last lane
      lane_capacity = [cars_per_lane for _ in range(num_lanes)]
      lane_capacity[-1] += extra_cars

      car_techniques = np.random.choice(["Reckless", "Cautious", "Normal"], num_cars, p=tecnhique_distrib)
      # get the number of cars of each category
      self.num_cars_by_technique["Reckless"] = np.sum(car_techniques == "Reckless")
      self.num_cars_by_technique["Cautious"] = np.sum(car_techniques == "Cautious")
      self.num_cars_by_technique["Normal"] = num_cars - self.num_cars_by_technique["Reckless"] - self.num_cars_by_technique["Cautious"]

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

      # Define a color map for each driving type
      
      # Plot cars
      for lane in range(self.num_lanes):
         lane_positions = positions[lane]
         driving_types = [self.cars[car_index].technique for car_index in self.lanes[lane]]
         colors = [self.driving_type_colors[driving_type] for driving_type in driving_types]
         plt.scatter(lane_positions, [lane * .05] * len(lane_positions), color=colors, label=f'Lane {lane}')
         
      # Add labels to plot
      plt.xlabel('Position')
      plt.ylabel('Lane')
      plt.title(f'{self.num_lanes} Lane Highway with {self.num_cars} Cars')
      plt.yticks([lane * .05 for lane in range(self.num_lanes)], [f"Lane{lane}" for lane in range(self.num_lanes)])


      # Show plot
      plt.tight_layout()
      ax = plt.gca()
      plt.show()
      # plt.ion()
      
      display.clear_output(wait=True)
      

   def update(self):
      """"Update the simulation by one time step"""
      # randomly update the order of the cars
      # update_order = np.random.permutation(np.arange(self.num_cars))
      waiting_cars = self.get_waiting_cars()
      self.num_waiting_per_timestep.append(len(waiting_cars))

      self.track_waiting_technique()


      update_order = []
      for lane in self.lanes:
         update_order += lane

      for i in update_order:
         car = self.cars[i]
         car.pos += car.speed

         # get the index of the car in front of them.
         car_index = self.lanes[car.lane].index(i)
         next_car_index = self.lanes[car.lane][(car_index + 1) % len(self.lanes[car.lane])]
         next_car = self.cars[next_car_index]

         dist_to_next_car = car.distance_to_car(next_car, self.lane_length)
         # if car's speed is slower than next car's speed, and they are within the threshold, then brake
         # car_a_velocity = car _a_velocity - deceleration_param * (1 / |car_b_position - car_a_position| **2)
         

         if ((dist_to_next_car) < car.threshold) and (car.speed > next_car.speed):
            # print(f"Car {i} is braking with a distance of {dist_to_next_car}")
            car.speed = max(car.speed - 2 * car.decel * (1 / dist_to_next_car ** 2), 0)
            if dist_to_next_car < car.length:
               car.speed = 0
            car.waiting_for += 1
         else:
            car.speed = min(car.desired_speed, car.speed + car.accel)
            car.waiting_for = 0

         # make sure the car is still in bounds
         car.check_bounds(self.lane_length)

         # make sure that the lane is updated correctly with which car is in front
         self.update_lanes()


   def get_waiting_cars(self):
      """Get the cars that are currently waiting to change lanes."""
      cars_waiting = []
      for lane in self.lanes:
         for car_index in lane:
            car = self.cars[car_index]
            if car.waiting_for >= car.patience:
               cars_waiting.append(car)
      return cars_waiting
   
   def get_waiting_technique(self):
      """Get the number of cars that are currently waiting to change lanes by technique."""
      reckless_waiting = 0
      cautious_waiting = 0
      normal_waiting = 0
      for lane in self.lanes:
         for car_index in lane:
            car = self.cars[car_index]
            if car.waiting_for >= car.patience:
               if car.technique == "Reckless":
                  reckless_waiting += 1
               elif car.technique == "Cautious":
                  cautious_waiting += 1
               else:
                  normal_waiting += 1
      return reckless_waiting, cautious_waiting, normal_waiting
   
   def track_waiting_technique(self):
      """Track the number of cars that are currently waiting to change lanes by technique."""
      reckless_waiting, cautious_waiting, normal_waiting = self.get_waiting_technique()
      self.num_waiting_by_tecnique["Reckless"].append(reckless_waiting)
      self.num_waiting_by_tecnique["Cautious"].append(cautious_waiting)
      self.num_waiting_by_tecnique["Normal"].append(normal_waiting)

   def update_lanes(self):
      for lane_num, lane in enumerate(self.lanes):
         self.lanes[lane_num].sort(key=lambda x: self.cars[x].pos)


   def run(self, num_steps, plot=True):
      for i in range(num_steps):
         # print(f"Update #{i}")
         self.update()
         if plot:
            self.plot()
         # time.sleep(0.1)
      self.plot_all_waiting()
      self.plot_waiting_by_technique()
   
   def plot_all_waiting(self):
      plt.close()
      plt.figure()
      plt.plot([val / self.num_cars for val in self.num_waiting_per_timestep])
      plt.xlabel('Time Step')
      plt.ylabel('Percent of Waiting Cars')
      plt.title('Percentage of Waiting Cars Over Time')
      plt.savefig('waiting_cars.png')

   def plot_waiting_by_technique(self):
      plt.close()
      plt.figure(figsize=(100, 5))
      reckless = [x / self.num_cars_by_technique["Reckless"] for x in self.num_waiting_by_tecnique["Reckless"]]
      cautious = [x / self.num_cars_by_technique["Cautious"] for x in self.num_waiting_by_tecnique["Cautious"]]
      normal = [x / self.num_cars_by_technique["Normal"] for x in self.num_waiting_by_tecnique["Normal"]]

      plt.plot(reckless, color='red', label='Reckless')
      plt.plot(cautious, color='green', label='Cautious')
      plt.plot(normal, color='blue', label='Normal')
      plt.xlabel('Time Step')
      plt.ylabel('Percent of Waiting Cars by Technique')
      plt.title('Percent of Waiting Cars Over Time by Technique')
      plt.savefig('waiting_cars_by_technique.png')
      




if __name__ == "__main__":
   highway_sim = Simulation(100, 1, [.3, .3, .4], 5, 125)
   highway_sim.run(1000, False)
   
   


