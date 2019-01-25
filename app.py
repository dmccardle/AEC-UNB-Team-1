from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('data.json')


@app.route('/app')
def hello_world():
    q = Query()

    result = (db.search(q.thing == 'val2'))
    for element in result:
        print(element['thing'])
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

@app.route('/app/submit')
def submit():
    requestType = request.args['type']
    if requestType == 'Calculate':
        return "Perform a calculation!"
    elif requestType == 'Export':
        return "Perform an export!"


if __name__ == '__main__':
    app.run()
