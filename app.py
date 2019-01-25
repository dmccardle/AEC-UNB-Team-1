from flask import Flask, render_template, request, send_from_directory, jsonify
from tinydb import TinyDB, Query
from data_processing import *
import os

app = Flask(__name__)
db = TinyDB('data.json')
dataProcessor = DataProcessor()
dataProcessor.calculate_cost(100000000, 'Type 1')

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
        json_turbine = {}
        json_optional = {}
        for value_in in request.form:
            split = value_in.split('_')
            print(split[0])
            if len(split) < 3: # represent budget or type 
                if split[0] == 'budget':
                    budget = request.form[split[0]]
            elif split[1] == 'turbine': # represents data for the turbines
                if split[2] not in json_turbine:
                    json_turbine[split[2]] = {}
                else:
                    json_turbine[split[2]][split[0]] = request.form[split[0]]
            else: # represents data for the optional costs
                if split[2] not in json_optional and split[2].isdigit():
                    json_optional[split[2]] = {}
                else:
                    json_optional[split[2]][split[0]] = request.form[split[0]]

        print(json_turbine)
        print(json_optional)
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
