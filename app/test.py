import unittest
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))
import app
import json
from http import HTTPStatus

class TestAPIMethods(unittest.TestCase):
    def setUp(self):
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        app.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app = app.app.test_client()
        app.db.create_all()
        cmd = "DROP TABLE IF EXISTS payment"
        result = app.db.engine.execute(cmd)
        cmd = """
            CREATE TABLE payment (
                accountNumber INTEGER PRIMARY KEY AUTOINCREMENT,
                currencyCode TEXT CHECK(currencyCode IN ('TRY', 'USD', 'EUR')),
                ownerName VARCHAR(128),
                accountType TEXT CHECK(accountType IN ('individual', 'corporate')),
                balance INTEGER DEFAULT 0,
                senderAccount INTEGER,
                receiverAccount INTEGER,
                amount INTEGER,
                transactionType TEXT CHECK(transactionType IN ('payment','deposit','withdraw')),
                createdAt DATE
            )
            """
        result = app.db.engine.execute(cmd)
        cmd = "INSERT INTO payment (accountNumber, currencyCode, ownerName, accountType, balance ,senderAccount, receiverAccount, amount, transactionType) values ('132629', 'TRY', 'John', 'individual', 0, NULL, NULL, NULL, NULL)"
        app.db.engine.execute(cmd)

    def test_get(self):
        result = app.account_info(132629)
        expected = json.dumps({
            "accountNumber": 132629,
            "currencyCode": "TRY", 
            "ownerName": "John",
            "accountType": "individual",
            "balance": 0}), HTTPStatus.OK 
        self.assertEqual(result, expected)

    def test_post(self): 
        result = app.create({
            "accountNumber": 447381,
            "currencyCode": "USD", 
            "ownerName": "Jennifer",
            "accountType": "corporate",
            "balance": 100})
        result = app.account_info(result.lastrowid)
        expected = json.dumps({
            "accountNumber": 447381,
            "currencyCode": "USD", 
            "ownerName": "Jennifer",
            "accountType": "corporate",
            "balance": 100
            }), HTTPStatus.OK    
        self.assertEqual(result, expected)    


if __name__ == '__main__':
    unittest.main()