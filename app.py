import requests
import json
from datetime import datetime
from flask import Flask, request, Response
from pymongo import MongoClient

app = Flask(__name__)

payments = 'http://localhost:4000/payments'

mongo = MongoClient('mongodb://34.159.173.53:27017/api')
db = mongo.admin

@app.route('/')
def index():
  return 'Server Running!'
  
@app.route('/greet')
def say_hello():
  return 'Hello from Server'

@app.route('/api', methods=['GET', 'POST'])
def api():
  if request.method == 'GET':
    # there should be validation for the user being authorized for this action prior to anything else
    data = requests.get(payments).text

    return Response(data, status=200)
  elif request.method == 'POST':
    # there should be validation for the user being authorized for this action prior to anything else
    id = request.form['referenceId']
    amount = request.form['amount']
    if not id:
      return Response(json.dumps({'error': 'reference ID not supplied'}), status=400)
    elif not amount or not amount.lstrip("-").isnumeric():
      return Response(json.dumps({'error': 'Error: payment amount not supplied or invalid'}), status=400)
    elif float(amount) < 0:
      return Response(json.dumps({'error': 'payment amount must be positive'}), status=400)
    
    value = {'referenceId': id, 'amount': amount}
    
    insert = requests.post(payments, json=value).text
    result = json.loads(insert)
    if result.get('error'):
      return Response(json.dumps({'error': result['error']}), status=400)
    else:
      try:
        None
        #db.payments.insert_one({'id': id, 'amount': amount, 'time': datetime.utcnow()})
      except:
        # local logging of issues goes here
        print('MongoLog error')
      return Response(f'Transaction {id} processing!', status=201)