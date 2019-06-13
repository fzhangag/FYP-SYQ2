from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

#from app import app

test = Flask(__name__)
test.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
test.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test.db'
db = SQLAlchemy(test)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False) 
    birth = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    goal = db.Column(db.String(10), nullable=False)
    modify = db.Column(db.String(10), nullable=False)
    

    def __init__(self, username, name, password, gender, birth, mobile, address, state, goal, modify):
    	self.username = username
    	self.name = name
    	self.gender = gender
    	self.password = password
    	self.birth = birth
    	self.mobile = mobile
    	self.address = address
    	self.state = state
    	self.goal = goal
    	self.modify = modify

    def is_authenticated(self):
    	return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_state(self):
    	return self.state


class employment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, nullable=False)
	employee_name = db.Column(db.String(120), nullable=False)
	employer_name = db.Column(db.String(120), nullable=False)
	company_name = db.Column(db.String(120), nullable=False)
	company_address = db.Column(db.String(120), nullable=False)
	employee_address = db.Column(db.String(120), nullable=False)
	job = db.Column(db.String(120), nullable=False)
	duty = db.Column(db.String(120), nullable=False)
	full = db.Column(db.String(120), nullable=False)
	work_hour = db.Column(db.String(120), nullable=False)
	salary = db.Column(db.String(120), nullable=False)
	annual_leave = db.Column(db.String(120), nullable=False)
	commence = db.Column(db.String(120), nullable=False)
	ddl = db.Column(db.String(120), nullable=False)
	remote = db.Column(db.String(120), nullable=False)
	work_place = db.Column(db.String(120), nullable=False)
	probationary = db.Column(db.String(120),nullable=False)
	duration = db.Column(db.String(120),nullable=False)
	advance = db.Column(db.String(120), nullable=False)
	insurance = db.Column(db.String(120), nullable=False)
	commission = db.Column(db.String(120), nullable=False)

	def __init__(self, userid, employee_name, employer_name, company_name, company_address, employee_address, job, duty, full, work_hour, salary, annual_leave, commence, ddl, remote, work_place, probationary, duration, advance, insurance, commission):
		self.userid = userid
		self.employee_name = employee_name
		self.employer_name = employer_name
		self.company_name = company_name
		self.company_address = company_address
		self.employee_address = employee_address
		self.job = job
		self.duty = duty
		self.full = full
		self.work_hour = work_hour
		self.salary = salary
		self.annual_leave = annual_leave
		self.commence = commence
		self.ddl = ddl
		self.remote = remote
		self.work_place = work_place
		self.probationary = probationary
		self.duration = duration
		self.advance = advance
		self.insurance = insurance
		self.commission = commission


class divorce(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, nullable=False)
	mother_name = db.Column(db.String(120), nullable=False)
	father_name = db.Column(db.String(120), nullable=False)
	mother_hkid = db.Column(db.String(120), nullable=False)
	mother_address = db.Column(db.String(120), nullable=False)
	father_hkid = db.Column(db.String(120), nullable=False)
	father_address = db.Column(db.String(120), nullable=False)
	mother_age = db.Column(db.String(120), nullable=False)
	father_age = db.Column(db.String(120), nullable=False)
	marriage_date = db.Column(db.String(120), nullable=False)
	num_child = db.Column(db.String(120), nullable=False)
	child_name = db.Column(db.String(120), nullable=False)
	born_date = db.Column(db.String(120), nullable=False)
	adopt = db.Column(db.String(120), nullable=False)
	children_maintence = db.Column(db.String(120), nullable=False)
	spousal_maintance= db.Column(db.String(120), nullable=False)
	spousal_much = db.Column(db.String(120), nullable=False)
	spousal_long = db.Column(db.String(120), nullable=False)
	mother_asset = db.Column(db.String(120), nullable=False)
	father_asset = db.Column(db.String(120), nullable=False)

	def __init__(self, userid, mother_name, father_name, mother_hkid, mother_address, father_hkid, father_address, mother_age, father_age, marriage_date, num_child, child_name, born_date, adopt, children_maintence, spousal_maintance, spousal_much, spousal_long, mother_asset, father_asset):
		self.userid = userid
		self.mother_name = mother_name
		self.father_name = father_name
		self.mother_hkid = mother_hkid
		self.mother_address = mother_address
		self.father_hkid = father_hkid
		self.father_address = father_address
		self.mother_age = mother_age
		self.father_age = father_age
		self.marriage_date = marriage_date
		self.num_child = num_child
		self.child_name = child_name
		self.born_date = born_date
		self.adopt = adopt
		self.children_maintence = children_maintence
		self.spousal_maintance = spousal_maintance
		self.spousal_much = spousal_much
		self.spousal_long = spousal_long
		self.mother_asset = mother_asset
		self.father_asset = father_asset




