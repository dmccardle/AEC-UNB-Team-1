from flask import Flask, render_template, request, send_from_directory, jsonify
from data_processing import *
import os
import json

# Initialize Flask Application
app = Flask(__name__)
# Setup data processor for performing data manipulations
dataProcessor = DataProcessor()
result = dataProcessor.calculate_cost(100000000, 'Type 1')

# App home screen
@app.route('/app')
def hello_world():
    return render_template('app.html')

# Performed when the user selects to 'calculate' or 'export'
@app.route('/app/submit',  methods=['POST'] )
def submit():
    # determines which type of request from the form and performs the operation
    requestType = request.form['type']

    if requestType == 'Calculate':
        # stores json data about each turbine type from the excel document
        json_turbine = {}
        # stores json data about each optional data type from the excel document
        json_optional = {}

        # process which form data is for the turbine, and which is for the optional data
        json_turbine, json_optional = process_form_data()

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

@app.route('/app/getresult')
def get_result():
    calculation_result = {}
    # Some of these are Numpy types which need unpacking with the item() function
    calculation_result['totalCost'] = result[0].item()
    calculation_result['numTurbines'] = result[1]
    calculation_result['locations'] = result[2]
    calculation_result['totalPower'] = result[3].item()
    calculation_result['totalTime'] = result[4].item()

    return json.dumps(calculation_result)

if __name__ == '__main__':
    app.run()

def process_form_data():
    # Format of value data: 
    COLUMN_INDEX = 0 # Represents the index for accessing a column ex. Cut-in wind speed
    TYPE_INDEX = 1 # Represents the type the data represents (turbine or optional costs)
    ROW_INDEX = 2 # Represents which turbine or optional cost this data is referencing
    
    # variables to store return values
    turbine_return_json = {}
    optional_return_json = {}

    for value in request.form:
        # Split the input value to allow for accessing each element in the string
        value_split = value.split('_')

        # If there are less than three strings, the data represents information about either 
        # the budget of the price per kwh
        if len(value_split) < 3:
            if value_split[COLUMN_INDEX] == 'budget':
                budget = request.form[value_split[COLUMN_INDEX]]
            elif value_split[COLUMN_INDEX] == 'profit':
                price_per_kwh = request.form[value_split[COLUMN_INDEX]]
        # Represents a value containing turbine information
        elif value_split[TYPE_INDEX] == 'turbine':
            if value_split[ROW_INDEX] not in turbine_return_json:
                turbine_return_json[value_split[ROW_INDEX]] = {}
            else:
                turbine_return_json[value_split[ROW_INDEX]][value_split[COLUMN_INDEX]] = request.form[value]
        # Represents a value containing optional data information
        else:
            if value_split[ROW_INDEX] not in optional_return_json:
                optional_return_json[value_split[ROW_INDEX]] = {}
            else:
               optional_return_json[value_split[ROW_INDEX]][value_split[COLUMN_INDEX]] = request.form[value]
        
    return turbine_return_json, optional_return_json
