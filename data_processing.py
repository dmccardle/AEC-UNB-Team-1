import pandas as pd
from statistics import stdev

class DataProcessor():
    def __init__(self):
        self.df_turbines = pd.read_excel('aec.xlsx', nrows=4)
        self.df_optional_costs = pd.read_excel('aec.xlsx', skiprows=11).dropna(axis=1)
        self.df_wind_data = pd.read_excel('aec.xlsx', sheet_name='wind-data', index_col=0)
        self.df_depth_data = pd.read_excel('aec.xlsx', sheet_name='depth-data', index_col=0)
        tmp = self.df_wind_data.values.reshape(1, -1)[0]  # flatten data points
        tmp = [x for x in tmp if isinstance(x, (int, float))]  # remove non-numbers
        self.wind_stdev = stdev(tmp)


    # Returns: all locations that have wind speed within one standard deviation of nominal_speed
    def find_location_candidates(self, lower_speed, upper_speed):
        to_return = []
        for index, val in enumerate(self.df_wind_data.values):
            for col_index, col_val in enumerate([x for x in list(val) if isinstance(x, (int, float))]):
                if lower_speed - self.wind_stdev < col_val < upper_speed + self.wind_stdev:
                    to_return.append((index, col_index))

        return to_return


    # Returns: Sorted depths at given locations from location_candidates
    def find_depth_candidates(self, location_candidates):
        depth = self.df_depth_data.values
        depth_dict = {}
        for i, j in location_candidates:
            depth_dict[(i,j)] = depth[i,j]
        return sorted(depth_dict.items(), key=lambda kv: kv[1])


    # Returns: List of turbines that can be bought under the budget
    def calculate_cost(self, budget, turbine_type):

        turbine = self.df_turbines.loc[self.df_turbines['Turbine Type'] == turbine_type]

        nominal_speed = turbine['Nominal power at (m/s)'].iloc[0]
        nominal_power = turbine['Nominal Power (kW)'].iloc[0]
        time_to_construct = turbine['Time to construct (years)'].iloc[0]
        type = turbine['Turbine Type'].iloc[0]


        if not isinstance(nominal_speed, (int, float)):
            speeds = list(map(int, nominal_speed.split(' to ')))
            location_candidates = self.find_location_candidates(speeds[0], speeds[1])
        else:
            location_candidates = self.find_location_candidates(nominal_speed, nominal_speed)


        depth_candidates = self.find_depth_candidates(location_candidates)

        # Indexes and columns variables hold the actual longitutde and latitude values
        # Since we've been using indexes until now.
        columns = list(self.df_wind_data)
        indexes = self.df_wind_data.index.values

        locations = []
        total_cost = 0
        total_power = 0
        total_time = 0
        for candidate_key in depth_candidates:
            cost = turbine['Unit Cost (Millions $)'].iloc[0] * 1000000
            cost += turbine['Cost per meter depth increase'].iloc[0] * candidate_key[1]

            if budget - total_cost - cost > 0:
                locations.append((indexes[candidate_key[0][0]], columns[candidate_key[0][1]]))
                total_cost += cost
                total_power += nominal_power
                total_time += time_to_construct
            else:
                return total_cost, len(locations), locations, total_power, total_time, type
