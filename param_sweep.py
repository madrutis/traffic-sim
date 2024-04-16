from simulation import Simulation
import numpy as np
import matplotlib.pyplot as plt
import sys

def parameter_sweep(path):
    # runs the simulation for 500 epochs with different distributions of reckless, cautious, and normal drivers
    reckless_probs = np.arange(0, 1.1, .1)
    cautious_probs = np.arange(0, 1.1, .1)
    runs = 0
    for reckless in reckless_probs:
        for cautious in cautious_probs:
            reckless = round(reckless, 2)
            cautious = round(cautious, 2)
            
            # normal + reckless + cautious must sum to 1
            normal = 1.0 - reckless - cautious
            if normal < 0:
                continue
            print(f"Runs #: {runs} and {runs+ 1} and {runs + 2}")
            print(f"reckless: {reckless}, cautious: {cautious}, normal: {normal}")
            
            # run the sim 3 times for each distribution of drivers
            for i in range(3):
                highway_sim = Simulation(30, 1, [reckless, cautious, normal], path, 3, 125)
                highway_sim.run(500, False, True)
                runs += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a path as a command line argument.")
        sys.exit(1)
    path = sys.argv[1]
    parameter_sweep(path)