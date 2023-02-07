import json
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [
        { 'id': 1, 'firstName': 'fn1', 'lastName':'ln1', 'emailId':'email1@gmail.com'},
        { 'id': 2, 'firstName': 'fn2', 'lastName':'ln2', 'emailId':'email2@gmail.com'},
        { 'id': 3, 'firstName': 'fn3', 'lastName':'ln3', 'emailId':'email3@gmail.com'}
]

nextEmployeeId = 4
cursor = None
conn = None
try:
  print("CONNEXION EN COURS")
  conn = psycopg2.connect(
    host="127.0.0.1",
    database="my_company_db",
    user="postgres",
    password="password",
    port="5432"
  )
  cursor = conn.cursor()
except:
  print("CONNEXION FOIREE")
try:
  print("ESSAI CREATION TABLE")
  cursor.execute('CREATE TABLE IF NOT EXISTS employees (id serial NOT NULL PRIMARY KEY, firstName varchar(255) NOT NULL, lastName varchar(255) NOT NULL, emailId varchar(255) NOT NULL);')
  conn.commit()
except:
  print("TABLE EXISTE DEJA")

cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS employees (id serial NOT NULL PRIMARY KEY, firstName varchar(255) NOT NULL, lastName varchar(255) NOT NULL, emailId varchar(255) NOT NULL);')
conn.commit()

@app.route('/insert')
def test():
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees(firstName, lastName, emailId) values ('fn1','ln1','em1')")
    conn.commit()

    return jsonify('success')

@app.route('/api/v1/employees', methods=['GET'])
def get_employees():
  return jsonify(employees)

@app.route('/api/v1/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id: int):
  employee = get_employee(id)
  if employee is None:
    return jsonify({ 'error': 'Employee does not exist'}), 404
  return jsonify(employee)

def get_employee(id):
  return next((e for e in employees if e['id'] == id), None)

def employee_is_valid(employee):
  print(employee)
  for key in employee.keys():
    if key != 'name':
      return False
  return True

@app.route('/api/v1/employees', methods=['POST'])
def create_employee():
  print("nouveau employé")
  global nextEmployeeId
  employee = json.loads(request.data)
  print(employee)
  if not employee_is_valid(employee):
    return jsonify({ 'error': 'Invalid employee properties.' }), 400

  employee['id'] = nextEmployeeId
  nextEmployeeId += 1
  employees.append(employee)

  return '', 201, { 'location': f'/api/v1/employees/{employee["id"]}' }

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
