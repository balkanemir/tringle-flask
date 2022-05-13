from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script._compat import text_type
from flask_script import Manager
import enum

import sys
sys.path.append("..")
from initialise import Initialise

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@tringle-db/payment'

init = Initialise()
app = init.db(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
handler = Manager(app)
handler.add_command('db', MigrateCommand)

class CurrencyCodeEnum(enum.Enum):
    TRY = 'TRY'
    USD = 'USD'
    EUR = 'EUR'

class AccountTypeEnum(enum.Enum):
    individual = 'individual'
    corporate = 'corporate'

class TransactionNameEnum(enum.Enum):
    payment = 'payment'
    deposit = 'deposit'
    withdraw = 'withdraw'

class Payment(db.Model):
    accountNumber = db.Column(db.Integer, primary_key=True)
    currencyCode = db.Column(db.Enum(CurrencyCodeEnum))
    ownerName = db.Column(db.String(128))
    accountType = db.Column(db.Enum(AccountTypeEnum))
    balance = db.Column(db.Integer)
    senderAccount = db.Column(db.Integer)
    receiverAccount = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    transactionType = db.Column(db.Enum(TransactionNameEnum))

if __name__ == '__main__':
    handler.run()