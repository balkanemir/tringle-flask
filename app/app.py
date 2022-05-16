from flask import Flask, request
import json
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
from initialise import Initialise
import datetime

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
        },
        {
            "rel": "self",
            "resource": "http://127.0.0.1:5050/accounting/" + str(accountNumber),
            "method": "GET"
        }
    ]

@app.route('/account', methods=['POST'])
def account_create():
    try: 
        data = request.get_json()
        sql = text('INSERT INTO payment (accountNumber, currencyCode, ownerName, accountType, balance ,senderAccount, receiverAccount, amount, transactionType) values (:accountNumber, :currencyCode, :ownerName, :accountType, 0, NULL, NULL, NULL, NULL)')
        result = db.engine.execute(
            sql,
            accountNumber = data['accountNumber'],
            currencyCode = data['currencyCode'],
            ownerName = data['ownerName'],
            accountType = data['accountType']
        )
        return json.dumps({"accountNumber": data['accountNumber'], "links": hateoas(data['accountNumber'])})
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND     



@app.route('/account/<accountNum>', methods=['GET'])
def account_info(accountNumber):
    try:
        sql = text('SELECT accountNumber, currencyCode, ownerName, accountType, balance FROM payment WHERE accountNumber=accountNumber')
        result = db.engine.execute(sql, accountNumber=accountNumber).fetchone()
        return json.dumps({"accountNumber": result.accountNumber, "currencyCode": result.currencyCode, "ownerName": result.ownerName, "accountType": result.accountType, "balance": result.balance}), HTTPStatus.OK
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND


@app.route('/payment', methods=['POST'])
def payment():
    try: 
        data = request.get_json()
        sendersql = text('UPDATE payment SET receiverAccount=:receiverAccount,senderAccount=:senderAccount, balance= balance - :amount , amount=:amount, transactionType="payment", createdAt=:createdAt WHERE accountNumber=:senderAccount' )
        result = db.engine.execute(
            sendersql,
            senderAccount = data['senderAccount'],
            receiverAccount = data['receiverAccount'],
            amount = data['amount'],
            createdAt = datetime.datetime.now(),

        )
        receiversql = text('UPDATE payment SET receiverAccount=:receiverAccount,senderAccount=:senderAccount, balance= balance + :amount , amount=:amount, transactionType="payment", createdAt=:createdAt WHERE accountNumber=:receiverAccount' )
        result = db.engine.execute(
            receiversql,
            senderAccount = data['senderAccount'],
            receiverAccount = data['receiverAccount'],
            amount = data['amount'],
            createdAt = datetime.datetime.now(),
        )
        return json.dumps({"senderAccount": data['senderAccount'], "links": hateoas(data['senderAccount'])})
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND      

@app.route('/deposit', methods=['POST'])
def deposit():
    try: 
        data = request.get_json()
        sql = text('UPDATE payment SET receiverAccount=NULL,senderAccount=NULL, balance= balance + :amount , amount=:amount, transactionType="deposit", createdAt=:createdAt WHERE accountNumber=:accountNumber' )
        result = db.engine.execute(
            sql,
            accountNumber = data['accountNumber'],
            amount = data['amount'],
            createdAt = datetime.datetime.now(),
        )
        return json.dumps({"accountNumber": data['accountNumber'], "links": hateoas(data['accountNumber'])})
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND      

@app.route('/withdraw', methods=['POST'])
def withdraw():
    try: 
        data = request.get_json()
        sql = text('UPDATE payment SET receiverAccount=NULL,senderAccount=NULL, balance= balance - :amount , amount=:amount, transactionType="withdraw", createdAt=:createdAt WHERE accountNumber=:accountNumber' )
        result = db.engine.execute(
            sql,
            accountNumber = data['accountNumber'],
            amount = data['amount'],
            createdAt = datetime.datetime.now(),
        )
        return json.dumps({"accountNumber": data['accountNumber'], "links": hateoas(data['accountNumber'])})
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND      

@app.route('/accounting/<accountNumber>', methods=['GET'])
def transaction(accountNumber):
    try:
        sql = text('SELECT accountNumber, amount, transactionType, createdAt FROM payment WHERE accountNumber=accountNumber')
        result = db.engine.execute(sql, accountNumber=accountNumber).fetchone()
        return json.dumps({"accountNumber": result.accountNumber, "amount": result.amount, "transactionType": result.transactionType, "createdAt": str(result.createdAt)}), HTTPStatus.OK
    except Exception as e:
        return json.dumps('Failed. ' + str(e)), HTTPStatus.NOT_FOUND