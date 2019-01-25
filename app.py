from flask import Flask, render_template, request, send_from_directory, jsonify
from tinydb import TinyDB, Query
import pandas as pd
import os

app = Flask(__name__)
db = TinyDB('data.json')
df_turbines = pd.read_excel('aec.xlsx', nrows=4)
df_optimal_costs = pd.read_excel('aec.xlsx', skiprows=11).dropna(axis=1)
df_wind_data = pd.read_excel('aec.xlsx', sheet_name='wind-data', index_col=0)
df_depth_data = pd.read_excel('aec.xlsx', sheet_name='depth-data', index_col=0)

@app.route('/app')
def hello_world():
    q = Query()
    print(df_turbines)
    print(df_optimal_costs)
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
