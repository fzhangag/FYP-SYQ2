import conversation
from sqlalchemy import text
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from test import db
from test import User, employment
import database
import xlrd
import os

def test_int(userid, state):
	try:
		conversation.sequence_d(userid, state, "1")
	except Exception as e:
		print("error when test integer, divorce!" + str(userid) + "!!" + str(state))
		print(e)
	try:
		conversation.sequence_e(userid, state, "1")
	except Exception as e:
		print("error when test integer, employment!" + str(userid) + "!!" + str(state))
		print(e)

def test_float(userid, state):
	try:
		conversation.sequence_d(userid, state, "0.5")
	except Exception as e:
		print("error when test float, divorce!" + str(userid) + "!!" + str(state))
		print(e)
	try:
		conversation.sequence_e(userid, state, "0.5")
	except Exception as e:
		print("error when test float, employment!" + str(userid) + "!!" + str(state))
		print(e)

def test_lint(userid, state):
	try:
		conversation.sequence_d(userid, state, "10000000")
	except Exception as e:
		print("error when test large integer, divorce!" + str(userid) + "!!" + str(state))
		print(e)
	try:
		conversation.sequence_e(userid, state, "10000000")
	except Exception as e:
		print("error when test large integer, employment!" + str(userid) + "!!" + str(state))
		print(e)

def test_lfloat(userid, state):
	try:
		conversation.sequence_d(userid, state, "999999999.9999999999")
	except Exception as e:
		print("error when test large float, divorce!" + str(userid) + "!!" + str(state))
		print(e)
	try:
		conversation.sequence_e(userid, state, "999999999.9999999999")
	except Exception as e:
		print("error when test large float, employment!" + str(userid) + "!!" + str(state))
		print(e)

def test_string(userid, state):
	try:
		conversation.sequence_d(userid, state, "hello world")
	except Exception as e:
		print("error when test string, divorce!" + str(userid) + "!!" + str(state))
		print(e)
	try:
		conversation.sequence_e(userid, state, "hello world")
	except Exception as e:
		print("error when test string, employment!" + str(userid) + "!!" + str(state))
		print(e)

def test_lstring(userid, state):
	try:
		conversation.sequence_d(userid, state, "hello world! I am a programmer from hkust and major in computer science! This is my final year project test part!")
	except Exception as e:
		print("error when test long string, divorce!" + str(userid) + "!!" + str(state))
		print(e)
	try:
		conversation.sequence_e(userid, state, "hello world! I am a programmer from hkust and major in computer science! This is my final year project test part!")
	except Exception as e:
		print("error when test long string, employment!" + str(userid) + "!!" + str(state))
		print(e)

def test_nint(userid, state):
	try:
		conversation.sequence_d(userid, state, "-1")
	except Exception as e:
		print("error when test negative integer, divorce!" + str(userid) + "!!" + str(state))
		print(e)
	try:
		conversation.sequence_e(userid, state, "-1")
	except Exception as e:
		print("error when test negative integer, employment!" + str(userid) + "!!" + str(state))
		print(e)

def test_nfloat(userid, state):
	try:
		conversation.sequence_d(userid, state, "-0.5")
	except Exception as e:
		print("error when test negative float, divorce!" + str(userid) + "!!" + str(state))
		print(e)
	try:
		conversation.sequence_e(userid, state, "-0.5")
	except Exception as e:
		print("error when test negative float, employment!" + str(userid) + "!!" + str(state))
		print(e)

def test_special(userid, state):
	try:
		conversation.sequence_d(userid, state, "$%@#")
	except Exception as e:
		print("error when test special character, divorce!" + str(userid) + "!!" + str(state))
		print(e)
	try:
		conversation.sequence_e(userid, state, "$%@#")
	except Exception as e:
		print("error when test special character, employment!" + str(userid) + "!!" + str(state))
		print(e)

def read_employment():
	file = os.getcwd()+'/test_data/AI-Sample-Data-Employment.xlsx'
	data = xlrd.open_workbook(file)
	table = data.sheets()[0]
	nrows = table.nrows
	result = []
	for i in range(1,nrows):
		x = table.row_values(i)
		if x[0].find("What's")!=-1:
			continue
		result.append(x)
	return result

def read_divorce():
	file = os.getcwd()+'/test_data/AI-Sample-Data-Marriage.xlsx'
	data = xlrd.open_workbook(file)
	table = data.sheets()[0]
	nrows = table.nrows
	result = []
	for i in range(1,nrows):
		x = table.row_values(i)
		if x[0].find("What's")!=-1:
			continue
		result.append(x)
	return result


sql = text("select * from User where username='test_chatbot'")
result = db.engine.execute(sql)
db.session.commit()
x = []
for row in result:
	x.append(row)

userid = ""
if len(x)==0:
	new_user = User("test_chatbot","0","0","0","0","0","0","not","not","0")
	db.session.add(new_user)
	db.session.commit()
	database.insert_employment(new_user.id)
	database.insert_divorce(new_user.id)
	userid = new_user.id
else:
	userid = x[0][0]


for i in range(1,20):
	print("for state "+str(i))
	test_int(userid,i)
	test_float(userid,i)
	test_lint(userid,i)
	test_lfloat(userid,i)
	test_string(userid,i)
	test_lstring(userid,i)
	test_nint(userid,i)
	test_nfloat(userid,i)
	test_special(userid,i)


employment_data = read_employment()
divorce_data = read_divorce()


for i in range(len(employment_data)):
	for j in range(1,len(employment_data[0])):
		try:
			conversation.sequence_e(userid, j, employment_data[i][j-1])
		except Exception as e:
			print(e)

for i in range(len(divorce_data)):
	for j in range(1,len(divorce_data[0])):
		try:
			conversation.sequence_d(userid, j, divorce_data[i][j-1])
		except Exception as e:
			print(e)




