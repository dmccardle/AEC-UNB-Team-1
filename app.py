from flask import Flask, render_template, request, send_from_directory, jsonify
from data_processing import *
import os
import json

app = Flask(__name__)
dataProcessor = DataProcessor()
result = dataProcessor.calculate_cost(100000000, 'Type 1')


@app.route('/app')
def hello_world():
    return render_template('app.html')

@app.route('/app/submit',  methods=['POST'] )
def submit():
    requestType = request.form['type']
    if requestType == 'Calculate':
        json_turbine = {}
        json_optional = {}

        for value_in in request.form:
            split = value_in.split('_')
            if len(split) < 3: # represent budget or type 
                if split[0] == 'budget':
                    budget = request.form[split[0]]
            elif split[1] == 'turbine': # represents data for the turbines
                if split[2] not in json_turbine:
                    json_turbine[split[2]] = {}
                else:
                    json_turbine[split[2]][split[0]] = request.form[value_in]
            else: # represents data for the optional costs
                if split[2] not in json_optional:
                    json_optional[split[2]] = {}
                else:
                    json_optional[split[2]][split[0]] = request.form[value_in]

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
