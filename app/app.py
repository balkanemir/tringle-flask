from flask import Flask, request
import json
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
from initialise import Initialise

app = Flask(__name__)
init = Initialise()
app = init.db(app)
db = SQLAlchemy(app)


def hateoas(accountNumber):
    return [
        {
            "rel": "self",
            "resource": "http://127.0.0.1:5050/account/" + str(accountNumber),
            "method": "GET"
        }
    ]

@app.route('/account', methods=['POST'])
def account_create():
    try: 
        data = request.get_json()
        sql = text('INSERT INTO payment (accountNumber, currencyCode, ownerName, accountType, balance ,senderAccount, receiverAccount, amount, transactionType) values (:accountNumber, :currencyCode, :ownerName, :accountType, NULL, NULL, NULL, NULL, NULL)')
        result = db.engine.execute(
            sql,
            accountNumber = data['accountNumber'],
            currencyCode = data['currencyCode'],
            ownerName = data['ownerName'],
            accountType = data['accountType']
        )
        return json.dumps({"accountNumber": result.lastrowid, "links": hateoas(result.lastrowid)})
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND     



@app.route('/account/<accountNumber>', methods=['GET'])
def account_info(accountNumber):
    try:
        sql = text('SELECT accountNumber, currencyCode, ownerName, accountType, balance FROM payment WHERE accountNumber=accountNumber')
        result = db.engine.execute(sql, accountNumber=accountNumber).fetchone()
        return json.dumps({"accountNumber": result.accountNumber, "currencyCode": result.currencyCode, "ownerName": result.ownerName, "accountType": result.accountType, "balance": result.balance}), HTTPStatus.OK
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND


@app.route('/payment', methods=['POST'])
def payment():
    pass  

@app.route('/deposit', methods=['POST'])
def deposit():
    pass

@app.route('/withdraw', methods=['POST'])
def withdraw():
    pass

@app.route('/accounting/<accountNumber>', methods=['GET'])
def transaction(accountNumber):
    pass