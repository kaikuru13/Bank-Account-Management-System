from flask import Flask, jsonify, request 
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy 

# Connect to the SQLite databse and create a SQLAlchemy model to represent the bank accounts: 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Bank_Users.db'
db = SQLAlchemy(app)

class bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pin = db.Column(db.Integer)
    balance = db.Column(db.Float)

    def __init__(self, username, pin, balance):
        self.username = username
        self.pin = pin
        self.balance = balance

class Login(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        pin = int(postedData["pin"])

        account = bank.query.filter_by(username=username, pin=pin).first()
        if account:
            return jsonify(status="success", message="logged in", username=account.username)
        else:
            return jsonify(status="fail", message="invalid username or pin")
class CreateAccount(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        pin = int(postedData["pin"])
        initial_deposit = postedData["initial_deposit"]

        account = bank.query.filter_by(username=username).first()
        if account:
            return jsonify(status="fail", message="username already exists")
        else:
            new_account = bank(username, pin, initial_deposit)
            db.session.add(new_account)
            db.session.commit()
            return jsonify(status="success", message="account created", username=new_account.username)

class CheckBalance(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]

        account = bank.query.filter_by(username=username).first()
        if account:
            return jsonify(status="success", balance=account.balance)
        else:
            return jsonify(status="fail", message="invalid username")

class Deposit(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        amount = postedData["amount"]

        account = bank.query.filter_by(username=username).first()
        if account:
            account.balance += amount
            db.session.commit()
            return jsonify(status="success", message="deposit successful", balance=account.balance)
        else:
            return jsonify(status="fail", message="invalid username")

class Withdraw(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        amount = postedData["amount"]

        account = bank.query.filter_by(username=username).first()
        if account:
            if account.balance >= amount:
                account.balance -= amount
                db.session.commit()
                return jsonify(status="success", message="withdrawal successful", balance=account.balance)
            else:
                return jsonify(status="fail", message="insufficient funds")
        else:
            return jsonify(status="fail", message="invalid username")


api = Api(app)
api.add_resource(Login, '/login')
api.add_resource(CreateAccount, '/create')
api.add_resource(CheckBalance, '/balance')
api.add_resource(Deposit, '/deposit')
api.add_resource(Withdraw, '/withdraw')

with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)