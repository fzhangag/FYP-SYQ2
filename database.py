import table
from table import db
from table import User
from table import employment
from table import divorce
from table import Name
from table import Organization
from sqlalchemy import text
from flask_login import login_manager

def insert_user():
	x = User('0','0','0','0','0','0','0','0','0','0')
	db.session.add(x)
	db.session.commit()

	return x.id

def update_user(userid, column, data):
	data = data.replace("'","''")
	sql = text("update User set " + column +" = '"+data+"' where id="+str(userid))
	db.engine.execute(sql)
	db.session.commit()

def get_user(userid, column):
	sql = text("select " + column +" from User where id="+str(userid))
	result = db.engine.execute(sql)
	x = []
	for row in result:
		x.append(row[0])
	return x

def get_user_id(username):
	sql = text("select id from User where username='"+username+"'")
	result = db.engine.execute(sql)
	x = []
	for row in result:
		x.append(row[0])

	if len(x)!=0:
		return x[0]
	else:
		return 0


def get_user_state(userid):
	state = get_user(userid, "state")
	try:
		state = int(state[0])
		return state
	except:
		return state[0]

def get_user_goal(userid):
	goal = get_user(userid, "goal")
	return goal[0]

def insert_name(name):
	name = name.replace("'","''")
	x = Name(name)
	db.session.add(x)
	db.session.commit()

	return x.id

def exist_userid(userid):
	sql = text("select * from User where id="+str(userid))
	result = db.engine.execute(sql)
	y = []
	for row in result:
		y.append(row[0])

	if len(y)!=0:
		return True
	else:
		return False

def exist_name(x):
	x = x.replace("'","''")
	sql = text("select name from Name where name='"+x+"'")
	result = db.engine.execute(sql)
	y = []
	for row in result:
		y.append(row[0])

	if len(y)!=0:
		return True
	else:
		return False

def insert_organization(y):
	y = y.replace("'","''")
	x = Organization(y)
	db.session.add(x)
	db.session.commit()

	return x.id

def exist_organization(x):
	x = x.replace("'","''")
	sql = text("select organization from Organization where organization='"+x+"'")
	result = db.engine.execute(sql)
	y = []
	for row in result:
		y.append(row[0])

	if len(y)!=0:
		return True
	else:
		return False


def insert_employment(userid):
	x = employment(userid,'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',1)
	db.session.add(x)
	db.session.commit()

	return x.id

def get_employ_column(userid, column):
	sql = text("select "+column+" from employment where userid="+str(userid))
	result = db.engine.execute(sql)
	db.session.commit()
	x = []
	for row in result:
		x.append(row[0])

	if len(x)!=0:
		return x[0]
	else:
		return 0

def update_employment(userid, column, data):
	if type(data) is not int:
		data = data.replace("'","''")
		sql = text("update employment set " + column +" = '"+data+"' where userid="+str(userid))
	else:
		sql = text("update employment set " + column +" = "+str(data)+" where userid="+str(userid))
	db.engine.execute(sql)
	db.session.commit()

def update_employment_info(userid, state, message):
	if state==1:
		update_employment(userid, "employee_name", message)
	elif state==2:
		update_employment(userid, "employer_name", message)
	elif state==3:
		update_employment(userid, "company_name", message)
	elif state==4:
		update_employment(userid, "company_address", message)
	elif state==5:
		update_employment(userid, "employee_address", message)
	elif state==6:
		update_employment(userid, "job", message)
	elif state==7:
		update_employment(userid, "duty", message)
	elif state==9:
		update_employment(userid, "work_hour", message)
	elif state==10:
		update_employment(userid, "salary", message)
	elif state==11:
		update_employment(userid, "annual_leave", message)
	elif state==12:
		update_employment(userid, "commence", message)
	elif state==13:
		update_employment(userid, "ddl", message)
	elif state==15:
		update_employment(userid, "work_place", message)
	elif state==17:
		update_employment(userid, "duration", message)
	elif state==18:
		update_employment(userid, "advance", message)
	elif state==19:
		update_employment(userid, "insurance", message)
	elif state==20:
		update_employment(userid, "commission", message)
	else:
		print("error!!!!!")

def get_employment(userid):
	sql = text("select * from employment where userid = "+str(userid))
	result = db.engine.execute(sql)
	db.session.commit()
	x = []
	for row in result:
		x.append(row)
	print(x)
	y = []
	y.append(x[0].employee_name)
	y.append(x[0].employer_name)
	y.append(x[0].company_name)
	y.append(x[0].company_address)
	y.append(x[0].employee_address)
	y.append(x[0].job)
	y.append(x[0].duty)
	y.append(x[0].full)
	y.append(x[0].work_hour)
	y.append(x[0].salary)
	y.append(x[0].annual_leave)
	y.append(x[0].commence)
	y.append(x[0].ddl)
	y.append(x[0].remote)
	y.append(x[0].work_place)
	y.append(x[0].probationary)
	y.append(x[0].duration)
	y.append(x[0].advance)
	y.append(x[0].insurance)
	y.append(x[0].commission)

	return y

def modify_employment(userid, num, message):
	print(message)
	num = int(num)
	if num==1:
		update_employment(userid, "employee_name", message)
	elif num==2:
		update_employment(userid, "employer_name", message)
	elif num==3:
		update_employment(userid, "company_name", message)
	elif num==4:
		update_employment(userid, "company_address", message)
	elif num==5:
		update_employment(userid, "employee_address", message)
	elif num==6:
		update_employment(userid, "job", message)
	elif num==7:
		update_employment(userid, "duty", message)
	elif num==8:
		update_employment(userid, "full", message)
	elif num==9:
		update_employment(userid, "salary", message)
	elif num==10:
		update_employment(userid, "annual_leave", message)
	elif num==11:
		update_employment(userid, "commence", message)
	elif num==12:
		update_employment(userid, "ddl", message)
	elif num==13:
		update_employment(userid, "remote", message)
	elif num==14:
		update_employment(userid, "probationary", message)
	elif num==15:
		update_employment(userid, "advance", message)
	elif num==16:
		update_employment(userid, "insurance", message)
	elif num==17:
		update_employment(userid, "commission", message)

	elif num==21:
		update_employment(userid, "work_hour", message)
	elif num==22:
		update_employment(userid, "work_place", message)
	elif num==23:
		update_employment(userid, "duration", message)
	else:
		print("error!!!!!")





def insert_divorce(userid):
	x = divorce(userid,'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',1)
	db.session.add(x)
	db.session.commit()

	return x.id

def update_divorce(userid, column, data):
	if type(data) is not int:
		data = data.replace("'","''")
		sql = text("update divorce set " + column +" = '"+data+"' where userid="+str(userid))
	else:
		sql = text("update divorce set " + column +" = "+str(data)+" where userid="+str(userid))
	db.engine.execute(sql)
	db.session.commit()

def get_divorce_child(userid):
	sql = text("select num_child from divorce where userid="+str(userid))
	result = db.engine.execute(sql)
	db.session.commit()
	x = []
	for row in result:
		x.append(row[0])

	if len(x)!=0:
		return x[0]
	else:
		return 0


def get_divorce_column(userid, column):
	sql = text("select "+column+" from divorce where userid="+str(userid))
	result = db.engine.execute(sql)
	db.session.commit()
	x = []
	for row in result:
		x.append(row[0])

	if len(x)!=0:
		return x[0]
	else:
		return 0

def update_divorce_info(userid, state, message):
	if state==1:
		update_divorce(userid, "mother_name", message)
	elif state==2:
		update_divorce(userid, "father_name", message)
	elif state==3:
		update_divorce(userid, "mother_hkid", message)
	elif state==4:
		update_divorce(userid, "mother_address", message)
	elif state==5:
		update_divorce(userid, "father_hkid", message)
	elif state==6:
		update_divorce(userid, "father_address", message)
	elif state==7:
		update_divorce(userid, "mother_age", message)
	elif state==8:
		update_divorce(userid, "father_age", message)
	elif state==9:
		update_divorce(userid, "marriage_date", message)
	elif state==10:
		update_divorce(userid, "num_child", message)
	elif state==11:
		update_divorce(userid, "child_name", message)
	elif state==12:
		update_divorce(userid, "born_date", message)
	# elif state==13:
	# 	update_divorce(userid, "adopt", message)
	# elif state==14:
	# 	update_divorce(userid, "children_maintence", message)
	elif state==15:
		update_divorce(userid, "spousal_maintance", message)
	elif state==16:
		update_divorce(userid, "spousal_much", message)
	elif state==17:
		update_divorce(userid, "spousal_long", message)
	elif state==18:
		update_divorce(userid, "mother_asset", message)
	elif state==19:
		update_divorce(userid, "father_asset", message)
	else:
		print("error!!!!!")

def get_divorce(userid):
	sql = text("select * from divorce where userid = "+str(userid))
	result = db.engine.execute(sql)
	db.session.commit()
	x = []
	for row in result:
		x.append(row)
	y = []
	y.append(str(x[0].mother_name))
	y.append(str(x[0].father_name))
	y.append(str(x[0].mother_hkid))
	y.append(str(x[0].mother_address))
	y.append(str(x[0].father_hkid))
	y.append(str(x[0].father_address))
	y.append(str(x[0].mother_age))
	y.append(str(x[0].father_age))
	y.append(str(x[0].marriage_date))
	y.append(str(x[0].num_child))
	y.append(str(x[0].child_name).split(";"))
	y.append(str(x[0].born_date).split(";"))
	y.append(str(x[0].university).split(";"))
	y.append(str(x[0].children_maintence).split(";"))
	y.append(str(x[0].child_main_who).split(";"))
	y.append(str(x[0].child_main_amount).split(";"))
	y.append(str(x[0].child_main_modify).split(";"))
	y.append(str(x[0].custody).split(";"))
	y.append(str(x[0].major_charge).split(";"))
	y.append(str(x[0].leave_hk).split(";"))
	y.append(str(x[0].where_live).split(";"))
	y.append(str(x[0].when_live).split(";"))
	y.append(str(x[0].child_access).split("|"))
	y.append(str(x[0].spousal_maintance))
	y.append(str(x[0].spousal_who))
	y.append(str(x[0].spousal_type))
	y.append(str(x[0].spousal_much))
	y.append(str(x[0].mother_asset).split(";"))
	y.append(str(x[0].father_asset).split(";"))

	return y

def modify_divorce(userid, num, message):
	print(message)
	state = int(num)
	if state==1:
		update_divorce(userid, "mother_name", message)
	elif state==2:
		update_divorce(userid, "father_name", message)
	elif state==3:
		update_divorce(userid, "mother_hkid", message)
	elif state==4:
		update_divorce(userid, "mother_address", message)
	elif state==5:
		update_divorce(userid, "father_hkid", message)
	elif state==6:
		update_divorce(userid, "father_address", message)
	elif state==7:
		update_divorce(userid, "mother_age", message)
	elif state==8:
		update_divorce(userid, "father_age", message)
	elif state==9:
		update_divorce(userid, "marriage_date", message)
	else:
		print("error!!!!!")


def update_user_first_sentiment(userid, data):
	sql = text("update User set first_sentiment="+str(data)+" where id="+str(userid))
	db.engine.execute(sql)
	db.session.commit()

def update_user_second_sentiment(userid, data):
	sql = text("update User set second_sentiment="+str(data)+" where id="+str(userid))
	db.engine.execute(sql)
	db.session.commit()


def get_user_first_sentiment(userid):
	goal = get_user(userid, "first_sentiment")
	return goal[0]

def get_user_second_sentiment(userid):
	goal = get_user(userid, "second_sentiment")
	return goal[0]

def clear_divorce(userid):
	sql = text("update divorce set mother_name='0', father_name='0', mother_hkid='0', mother_address='0', father_hkid='0', father_hkid='0', mother_asset='0', mother_age='0', father_asset='0', father_age='0', marriage_date='0', num_child='0', child_name='0', born_date='0', university='0', custody='0', major_charge='0', leave_hk='0', where_live='0', when_live='0', child_access='0', children_maintence='0', child_main_who='0', child_main_amount='0', child_main_modify='0', spousal_maintance='0', spousal_who='0', spousal_type='0', spousal_much='0' where userid='"+str(userid)+"'")
	db.engine.execute(sql)
	db.session.commit()

def clear_employment(userid):
	sql = text("update employment set employee_name='0', employer_name='0', company_name='0', company_address='0', employee_address='0', job='0', duty='0', full='0', work_hour='0', salary='0', annual_leave='0', commence='0', ddl='0', remote='0', work_place='0', probationary='0', duration='0', advance='0', insurance='0', commission='0' where userid='"+str(userid)+"'")
	db.engine.execute(sql)
	db.session.commit()

def clear_user(userid):
	sql = text("update User set state='not',goal='not',modify='0',first_sentiment=0, second_sentiment=0 where id='"+str(userid)+"'")
	db.engine.execute(sql)
	db.session.commit()

def delete_guest_user(userid):
	sql = text("delete from divorce where userid='" + str(userid) + "'")
	db.engine.execute(sql)
	db.session.commit()

	sql = text("delete from employment where userid='" + str(userid) + "'")
	db.engine.execute(sql)
	db.session.commit()

	sql = text("delete from User where id='" + str(userid) + "'")
	db.engine.execute(sql)
	db.session.commit()

def get_all_user_id():
	sql = text("select id from User")
	result = db.engine.execute(sql)
	x = []
	for row in result:
		x.append(row[0])
	return x

def get_user_guest(userid):
	guest = get_user(userid, "guest")
	return guest[0]

def update_user_last_modify(userid, data):
	sql = text("update User set last_modify='"+data.strftime('%Y-%m-%d %H:%M:%S.%f')+"' where id="+str(userid))
	db.engine.execute(sql)
	db.session.commit()

def get_user_last_modify(userid):
	last_modify = get_user(userid, "last_modify")
	return last_modify[0]











