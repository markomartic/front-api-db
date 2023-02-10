import json
import psycopg2
from flask import Flask, jsonify, request
import metier

app = Flask(__name__)
db = metier.DatabaseFactory.build_db("postgres")

@app.route('/api/v1/employees', methods=['GET'])
def get_all_clients():
  return jsonify(db.get_all_clients())
  
@app.route('/api/v1/employees/<int:id>', methods=['GET'])
def get_client(id):
    res = db.get_client(id)
    if(res == None):
        return jsonify({ 'error': 'Invalid request.' }), 400
    return jsonify(db.get_client(id))

@app.route('/api/v1/employees', methods=['POST'])
def add_client():
  jdata = json.loads(request.data)
  new_client = metier.ClientFactory.json2client(jdata)
  if(new_client == None):
      return jsonify({ 'error': 'Invalid client properties.' }), 400
  db.add_client(new_client) # TODO : check if worked well
  return jsonify("client added")

@app.route('/api/v1/employees/<int:id>', methods=['PUT'])
def update_client(id: int):
    return jsonify({ 'error': 'Feature not implemented yet.' }), 404

if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port=80)
