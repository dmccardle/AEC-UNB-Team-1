from flask import Flask, render_template, request, send_from_directory, jsonify
from data_processing import *
import os

app = Flask(__name__)
dataProcessor = DataProcessor()
dataProcessor.calculate_cost(100000000, 'Type 1')

@app.route('/app')
def hello_world():
    return render_template('app.html')

@app.route('/app/submit',  methods=['POST'] )
def submit():
    requestType = request.form['type']
    if requestType == 'Calculate':
        json_turbine = {}
        json_optional = {}

        COLUMN_INDEX = 0 # Represents the index for accessing a column ex. Cut-in wind speed
        TYPE_INDEX = 1 # Represents the type the data represents (turbine or optional costs)
        ROW_INDEX = 2 # Represents which turbine or optional cost this data is referencing
        
        for value_in in request.form:
            split = value_in.split('_')
            
            if len(split) < 3: # represent budget or type 
                if split[COLUMN_INDEX] == 'budget':
                    budget = request.form[split[COLUMN_INDEX]]
                elif split[COLUMN_INDEX] == 'profit':
                    price_per_kwh = request.form[split[COLUMN_INDEX]]

            elif split[TYPE_INDEX] == 'turbine': # represents data for the turbines
                if split[ROW_INDEX] not in json_turbine:
                    json_turbine[split[ROW_INDEX]] = {}
                else:
                    json_turbine[split[ROW_INDEX]][split[COLUMN_INDEX]] = request.form[value_in]

            else: # represents data for the optional costs
                if split[ROW_INDEX] not in json_optional:
                    json_optional[split[ROW_INDEX]] = {}
                else:
                    json_optional[split[ROW_INDEX]][split[COLUMN_INDEX]] = request.form[value_in]

        # Modify Turbine information tables
        for turbine in json_turbine:
            row = dataProcessor.df_turbines.loc[dataProcessor.df_turbines['Turbine Type'] == turbine]
            
            for attribute in json_turbine[turbine]:
                row[attribute].iloc[0] = json_turbine[turbine][attribute]

            dataProcessor.df_turbines.loc[dataProcessor.df_turbines['Turbine Type'] == turbine] = row

        # Modify Optional Cost information tables
        for option in json_optional:
            row = dataProcessor.df_optional_costs.loc[dataProcessor.df_optional_costs['Type'] == option]
            
            for attribute in json_optional[option]:
                row[attribute].iloc[0] = json_optional[option][attribute]

            dataProcessor.df_optional_costs.loc[dataProcessor.df_optional_costs['Type'] == option] = row

        return "Perform a calculation!"
    elif requestType == 'Export':
        return "Perform an export!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/app/get_turbine_data')
def turbine_data():
    return dataProcessor.df_turbines.to_json()

@app.route('/app/get_optional_cost_data')
def optional_cost_data():
    return dataProcessor.df_optional_costs.to_json()

if __name__ == '__main__':
    app.run()
