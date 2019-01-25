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
    q = Query()
    dataProcessor.find_location_candidates(15)
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
