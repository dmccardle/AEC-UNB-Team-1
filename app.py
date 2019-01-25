from flask import Flask, render_template, request, send_from_directory, jsonify
from tinydb import TinyDB, Query
from data_processing import *
import os
import json

app = Flask(__name__)
db = TinyDB('data.json')
dataProcessor = DataProcessor()
result = dataProcessor.calculate_cost(100000000, 'Type 1')


@app.route('/app')
def hello_world():
    return render_template('app.html')

@app.route( '/app/addEvent', methods=['POST'] )
def add_event():
    db.insert( request.get_json() )
    return jsonify(success=True)

@app.route('/app/fetch')
def getEvents():
    query = Query()

    result = db.all()
    return jsonify(result)

@app.route('/app/submit',  methods=['POST'] )
def submit():
    requestType = request.form['type']
    if requestType == 'Calculate':
        print(request.form)
        json_representation = {}
        for value_in in request.form:
            split = value_in.split('_')
            for i, token in enumerate(reversed(split)):

                if token not in json_representation and i == 0:
                    json_representation[token] = {}
        
        print(json_representation)
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
