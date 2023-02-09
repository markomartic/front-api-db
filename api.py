import json
import psycopg2
from flask import Flask, jsonify, request
import metier

app = Flask(__name__)
db = metier.DatabaseFactory.build_db("postgres")

@app.route('/api/v1/employees', methods=['GET'])
def get_employees():
  return jsonify(db.get_all_clients())
  
@app.route('/api/v1/employees/<int:id>', methods=['GET'])
def get_employee(id):
  return jsonify(db.get_client(id))

@app.route('/api/v1/employees', methods=['POST'])
def create_employee():
  employee = json.loads(request.data)
  print(f"create : {employee}")
  return jsonify({ 'error': 'Invalid employee properties.' }), 400
  return f'{employee}', 201, { 'location': f'/api/v1/employees/{employee["id"]}' }

@app.route('/api/v1/employees/<int:id>', methods=['PUT'])
def update_employee(id: int):
  employee = get_employee(id)
  if employee is None:
    return jsonify({ 'error': 'Employee does not exist.' }), 404

  updated_employee = json.loads(request.data)
  if not employee_is_valid(updated_employee):
    return jsonify({ 'error': 'Invalid employee properties.' }), 400

  employee.update(updated_employee)

  return jsonify(employee)

@app.route('/api/v1/employees/<int:id>', methods=['DELETE'])
def delete_employee(id: int):
  global employees
  employee = get_employee(id)
  if employee is None:
    return jsonify({ 'error': 'Employee does not exist.' }), 404

  employees = [e for e in employees if e['id'] != id]
  return jsonify(employee), 200

if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080)
