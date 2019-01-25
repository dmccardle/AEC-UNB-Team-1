from flask import Flask, render_template, request, send_from_directory, jsonify
from tinydb import TinyDB, Query
import pandas as pd
import os

app = Flask(__name__)
db = TinyDB('data.json')
df_turbines = pd.read_excel('aec.xlsx', nrows=4)
df_optional_costs = pd.read_excel('aec.xlsx', skiprows=11).dropna(axis=1)
df_wind_data = pd.read_excel('aec.xlsx', sheet_name='wind-data', index_col=0)
df_depth_data = pd.read_excel('aec.xlsx', sheet_name='depth-data', index_col=0)

@app.route('/app')
def hello_world():
    q = Query()
    print(df_turbines)
    print(df_optional_costs)
    print(df_wind_data.iloc[1])
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
    return df_turbines.to_json()

@app.route('/app/get_optional_cost_data')
def optional_cost_data():
    return df_optional_costs.to_json()

if __name__ == '__main__':
    app.run()
