#!/usr/bin/env python3
import pandas
import sys


def init_df(path):
    df = pandas.DataFrame(columns=['num_epochs','num_cars','reckless', 'cautious', 'normal', 'avg_diff_speed_reckless', 'avg_diff_speed_cautious', 'avg_diff_speed_normal'])
    df.to_csv(f'data/{path}', index=False)



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a path as a command line argument.")
        sys.exit(1)
    path = sys.argv[1]
    init_df(path)