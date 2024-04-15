import pandas

def init_df():
    df = pandas.DataFrame(columns=['num_cars','reckless', 'cautious', 'normal', 'avg_diff_speed_reckless', 'avg_diff_speed_cautious', 'avg_diff_speed_normal'])
    df.to_csv('data.csv', index=False)


if __name__ == '__main__':
    init_df()