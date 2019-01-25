from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query
import pandas as pd

app = Flask(__name__)
db = TinyDB('data.json')
df_turbines = pd.read_excel('aec.xlsx', nrows=4)
df_optimal_costs = pd.read_excel('aec.xlsx', skiprows=11).dropna(axis=1)



@app.route('/app')
def hello_world():
    q = Query()
    print(df_turbines)
    print(df_optimal_costs)
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


if __name__ == '__main__':
    app.run()
