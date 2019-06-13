from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


test = Flask(__name__)
test.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
test.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(test)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    goal = db.Column(db.String(10), nullable=False)

    def __init__(self, name, email, password, address, state, goal):
    	self.username = name
    	self.email = email
    	self.password = password
    	self.address = address
    	self.state = state
    	self.goal = goal

db.init_app(test)
x = User("Mary","aaa@aaa.com","11111","hkust","0","1")
db.create_all()
db.session.add(x)
db.session.commit()
sql = text("select username from User where id=1")
result = db.engine.execute(sql)
x = []
for row in result:
    x.append(row[0])
print(x)