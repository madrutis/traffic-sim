import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import IPython.display as display
import random as rand
from pprint import pprint
import time
import pandas as pd

#%matplotlib

class Car:
   reckless = {"desired_speed": 1, "accel": .2, "decel": .7, "threshold": 10, "patience": 5}
   cautious = {"desired_speed": 1, "accel": .03, "decel": .3, "threshold": 30, "patience": 12}
   normal = {"desired_speed": 1, "accel": .1, "decel": .4, "threshold": 18, "patience": 8}

   def __init__(self, lane, position, speed, technique, index, length=1):
      self.index = index
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
      # get dataframe
      self.data = self.load_csv()
      
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
      self.avg_diff_in_speed_per_timestep = {"Reckless": [], "Cautious": [], "Normal": []}

      self.lane_length = lane_length
      cars_per_lane = num_cars // num_lanes
      # cars that don't evenly fit in the lanes
      extra_cars = num_cars % num_lanes

      # add extra cars to the last lane
      lane_capacity = [cars_per_lane for _ in range(num_lanes)]
      lane_capacity[-1] += extra_cars

      self.technique_distrib = tecnhique_distrib
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
            new_car = Car(lane, position, speed, car_techniques[car_index], car_index, car_length)
            self.cars[car_index] = new_car
            self.lanes[lane].append(car_index)
            car_index += 1
            position += car_length + space_between_car
      
   def plot(self, timestep):
      positions = [[] for _ in range(self.num_lanes)]
      for lane_num, lane in enumerate(self.lanes):
         for car_index in lane:
            positions[lane_num].append(self.cars[car_index].pos)
      
      plt.figure(figsize=(10, 3))  # Adjust figure size if needed

      # Plot road lines for each lane
      for lane in range(self.num_lanes):
         plt.plot([0, self.lane_length], [lane * .05, lane * .05], color='gray', linestyle='--', linewidth=1)

      # Define a color map for each driving type
      
      # Plot cars based on technique
      for lane in range(self.num_lanes):
         lane_positions = positions[lane]
         driving_types = [self.cars[car_index].technique for car_index in self.lanes[lane]]
         colors = [self.driving_type_colors[driving_type] for driving_type in driving_types]
         plt.scatter(lane_positions, [lane * .05] * len(lane_positions), color=colors, label=f'Lane {lane}')

      # # Plot cars based on whether they are waiting
      # for lane in range(self.num_lanes):
      #    lane_positions = positions[lane]
      #    are_waiting = [self.cars[car_index].waiting_for >= self.cars[car_index].patience for car_index in self.lanes[lane]]
      #    colors = ['red' if waiting else 'yellow' for waiting in are_waiting]
      #    plt.scatter(lane_positions, [lane * .05] * len(lane_positions), color=colors, label=f'Lane {lane}')

      # Add labels to plot
      plt.xlabel('Position')
      plt.ylabel('Lane')
      plt.title(f'{self.num_lanes} Lane Highway with {self.num_cars} Cars at timestep {timestep}')
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
      
      # track waiting technique
      self.track_waiting_technique()
      
      # track difference in average speed
      reck_diff, caut_diff, norm_diff = self.get_difference_in_desired_speed()
      self.avg_diff_in_speed_per_timestep["Reckless"].append(reck_diff)
      self.avg_diff_in_speed_per_timestep["Cautious"].append(caut_diff)
      self.avg_diff_in_speed_per_timestep["Normal"].append(norm_diff)
      
      # have cars switch lanes if possible
      self.switch_lanes(waiting_cars)


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
            # car.waiting_for = 0

         # make sure the car is still in bounds
         car.check_bounds(self.lane_length)

         # make sure that the lane is updated correctly with which car is in front
         self.update_lanes()

   def switch_lanes(self, waiting_cars):
      """Try and switch the lane for all of the waiting cars."""
      for car in waiting_cars:
         # current lane
         current_lane = car.lane
         
         # get the target lane(s)
         target_lanes = []
         if current_lane == 0:
            target_lanes = [1]
         elif current_lane == self.num_lanes - 1:
            target_lanes = [self.num_lanes - 2]
         else:
            target_lanes = [current_lane + 1, current_lane - 1]
            # randomize the order of the target lanes
            # if np.random.random() < 0.5:
            #    target_lanes = target_lane[::-1]

            #
            if len(self.lanes[target_lanes[1]]) < len(self.lanes[target_lanes[0]]):
               target_lanes = target_lanes[::-1]
            
            # pick the lane with less people in it!

         
         # check to see if the target lane is available
         for target_lane in target_lanes:
            lane_availabe = True
            for neighbor_index in self.lanes[target_lane]:
               neighbor = self.cars[neighbor_index]
               # check to see if the adjacent spot is open
               if neighbor.pos > car.pos and neighbor.pos < (car.pos + (car.length / 2)):
                  lane_availabe = False
                  break
            if lane_availabe:
               self.swap_individual_car(car, target_lane)
               break

   def swap_individual_car(self, car, target_lane):
      """Swap the car from the current lane to the target lane."""
      car_index = car.index
      current_lane = car.lane
      self.lanes[current_lane].remove(car_index)
      self.lanes[target_lane].append(car_index)
      car.lane = target_lane
      car.waiting_for = 0
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
   
   def get_difference_in_desired_speed(self):
      """Get the avg(sum|speed - desired_speed|) of each type of driver."""
      reckless_speed_diff = 0
      cautious_speed_diff = 0
      normal_speed_diff = 0
      num_reck, num_cautious, num_normal = 0, 0, 0
      for lane in self.lanes:
         for car_index in lane:
            car = self.cars[car_index]
            if car.technique == "Reckless":
               reckless_speed_diff += abs(car.speed - car.desired_speed)
               num_reck += 1
            elif car.technique == "Cautious":
               cautious_speed_diff += abs(car.speed - car.desired_speed)
               num_cautious += 1
            else:
               normal_speed_diff += abs(car.speed - car.desired_speed)
               num_normal += 1
      reckless_avg = reckless_speed_diff / num_reck if num_reck > 0 else 0
      cautious_avg = cautious_speed_diff / num_cautious if num_cautious > 0 else 0
      normal_avg = normal_speed_diff / num_normal if num_normal > 0 else 0
      return reckless_avg, cautious_avg, normal_avg
   
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
            self.plot(i)
         # time.sleep(0.1)
      self.plot_all_waiting()
      self.plot_waiting_by_technique()
      self.plot_avg_diff_in_speed()
   
   def load_csv(self):
      return pd.read_csv('data.csv')

   def save_csv(self):
      pd.DataFrame(self.data).to_csv('data.csv', index=False)
   
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
      
   def plot_avg_diff_in_speed(self):
      """Plot the average difference in desired speed and actual speed and add to the dataframe."""
      plt.close()
      plt.figure(figsize=(100, 5))
      reckless = self.avg_diff_in_speed_per_timestep["Reckless"]
      cautious = self.avg_diff_in_speed_per_timestep["Cautious"]
      normal = self.avg_diff_in_speed_per_timestep["Normal"]

      plt.plot(reckless, color='red', label='Reckless')
      plt.plot(cautious, color='green', label='Cautious')
      plt.plot(normal, color='blue', label='Normal')
      plt.xlabel('Time Step')
      plt.ylabel('Average Difference in Desired Speed and Actual Speed')
      plt.title('Average Difference in Desired Speed and Actual Speed of All Cars By Tecnique')
      plt.savefig('avg_diff_desired_actual.png')
      print("Sum of average Difference in Speed:")
      sum_reckless = np.sum(reckless)
      sum_cautious = np.sum(cautious)
      sum_normal = np.sum(normal)
      print(f"Reckless: {sum_reckless}\tCautious: {sum_cautious}\tNormal: {np.sum(sum_normal)}")
      new_data = {}
      new_data['num_cars'] = self.num_cars
      reck_d, caut_d, norm_d = self.technique_distrib
      new_data['reckless'] = reck_d
      new_data['cautious'] = caut_d
      new_data['']
      self.data = self.data.append({'num_cars': self.num_cars, 'reckless': sum_reckless, 'cautious': sum_cautious, 'normal': sum_normal}, ignore_index=True)



if __name__ == "__main__":
   highway_sim = Simulation(30, 1, [1, 0, 0], 3, 125)
   highway_sim.run(500, True)
   
   


