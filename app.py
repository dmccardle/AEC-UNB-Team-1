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

if __name__ == '__main__':
    app.run()
