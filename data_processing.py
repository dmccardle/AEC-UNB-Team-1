import pandas as pd
from statistics import stdev

class DataProcessor():
    def __init__(self):
        self.df_turbines = pd.read_excel('aec.xlsx', nrows=4)
        self.df_optimal_costs = pd.read_excel('aec.xlsx', skiprows=11).dropna(axis=1)
        self.df_wind_data = pd.read_excel('aec.xlsx', sheet_name='wind-data', index_col=0)
        self.df_depth_data = pd.read_excel('aec.xlsx', sheet_name='depth-data', index_col=0)
        tmp = self.df_wind_data.values.reshape(1, -1)[0]  # flatten data points
        tmp = [x for x in tmp if isinstance(x, (int, float))]  # remove non-numbers
        self.wind_stdev = stdev(tmp)

    def find_location_candidates(self, nominal_speed):
        for a in self.df_wind_data.itertuples():
            print(a)
