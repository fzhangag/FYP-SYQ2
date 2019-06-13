import user
import pdf_employment
import pdf_divorce
import conversation
from flask import Flask, url_for, render_template, request, redirect, session, jsonify, make_response, \
    send_from_directory, send_file
import os
import webbrowser
from flask_sqlalchemy import SQLAlchemy
import table
from table import db
from sqlalchemy import text
import json
import database
import nltk
from nltk.corpus import names
from spacy.tokens import Doc
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from flask_login import LoginManager, current_user, login_required, UserMixin, login_user, logout_user, \
    AnonymousUserMixin
import flask_login
from apscheduler.schedulers.background import BackgroundScheduler

from table import User, employment
import database
import test_nlp

import spacy
from spacy.lang.en.examples import sentences
import en_core_web_sm

import datetime

DATABASE_CLEAR_INTERVAL = 43200
EXPIRE_TIME = 43200

app = Flask(__name__)
app.secret_key = "super secret key"

db.init_app(app)
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


login_manager.login_view = "login"
login_manager.session_protection = 'strong'


@app.route('/')
def home():
    return render_template('homepage.html', log="Log In")


@app.route('/backToHome')
def backToHome():
    return render_template('home.html', log="Log In")


@app.route('/humanistic_care')
def humanistic_care():
    return render_template('humanistic_care.html', log="Log In")


@app.route('/faq')
def faq():
    return render_template('FAQ.html', log="Log In")


@app.route('/contact')
def contact():
    return render_template('contacts.html', log="Log In")

@app.route('/restartChat', methods=['GET', 'POST'])
def restartChat():
    if request.method == 'POST':
        userid = current_user.get_id()
        if userid != None:
            goal = database.get_user_goal(userid)
            database.clear_divorce(userid)
            database.clear_employment(userid)
            database.update_user(userid, "goal", goal)
            if goal.find("not")!=-1:
                    state = "not"
            else:
                    state = "0"
            database.update_user(userid, "state", state)
        else:
            ip = request.remote_addr
            sql = text("select * from User where username='" + ip + "'")
            result = db.engine.execute(sql)
            db.session.commit()
            x = []
            for row in result:
                x.append(row)

            if len(x) == 0:
                print("into new guest user!")
                new_user = User(str(request.remote_addr), "0", "0", "0", "0", "0", "0", "not", "not", "0", 0, 0, True,
                                datetime.datetime.now())
                db.session.add(new_user)
                db.session.commit()
                database.insert_employment(new_user.id)
                database.insert_divorce(new_user.id)

                userid = new_user.id
            else:
                userid = x[0][0]

            goal = database.get_user_goal(userid)

            database.clear_divorce(userid)
            database.clear_employment(userid)
            database.update_user(userid, "goal", goal)
            if goal.find("not")!=-1:
                    state = "not"
            else:
                    state = "0"
            database.update_user(userid, "state", state)

        return jsonify({"returnMSG": "home"})


@app.route('/decideGoal', methods=['GET', 'POST'])
def decideGoal():
    if request.method == 'POST':
        goal = request.form['goal']
        userid = current_user.get_id()
        print("userID: " + str(userid))
        print("setGoal: " + goal)
        if userid != None:
            database.clear_divorce(userid)
            database.clear_employment(userid)
            database.update_user(userid, "goal", goal)
            if goal.find("not")!=-1:
                state = "not"
            else:
                state = "0"
            database.update_user(userid, "state", state)
        else:
            ip = request.remote_addr

            sql = text("select * from User where username='" + ip + "'")
            result = db.engine.execute(sql)
            db.session.commit()
            x = []
            for row in result:
                x.append(row)
            print(x)
            if len(x) == 0:
                print("into new guest user in backend with function-->decideGoal!")
                new_user = User(str(request.remote_addr), "0", "0", "0", "0", "0", "0", "not", goal, "0", 0, 0, True,
                                datetime.datetime.now())
                db.session.add(new_user)
                db.session.commit()
                database.insert_employment(new_user.id)
                database.insert_divorce(new_user.id)
                userid = new_user.id
            else:
                userid = x[0][0]
                database.clear_employment(userid)
                database.clear_divorce(userid)
            if goal.find('not') != -1:
                state = 'not'
            else:
                state = '0'
            database.update_user(userid, "goal", goal)
            database.update_user(userid, "state", state)

        if goal == "divorce":
            return jsonify({"returnMSG": "humanistic_care"})
        else:
            return jsonify({"returnMSG": "home"})


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        userid = request.form['username']
        passw = request.form['password']
        try:
            sql = text("select * from User where username = '" + userid + "' and password = '" + passw + "'")
            data = db.engine.execute(sql)
            db.session.commit()
            x = []
            for row in data:
                x.append(row)
            if len(x) != 0:
                print("log in success")
                session['logged_in'] = True
                user = load_user(x[0].id)

                user.id = x[0].id

                login_user(user, remember=True)
                database.update_user(user.id, "state", "0")

                print(current_user.id)
                return redirect(url_for('home'))
            else:
                return 'Not a registered user'
                return redirect(url_for('log_in'))
        except Exception as err:
            return "Not a registered user"
            return redirect(url_for('log_in'))
    return render_template('log_in.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    logout_user()
    # return "You have logged out already"
    return redirect(url_for('home'))


@app.route('/changepwd', methods=['GET', 'POST'])
def changepwd():
    if request.method == 'POST':
        oldpwd = request.form['oldpwd']
        newpwd = request.form['newpwd']
        confirmpwd = request.form['confirmpwd']
        if oldpwd == newpwd:
            return jsonify({"validation": "Same_pwd", "res": "Please enter correct old password."})
        elif newpwd != confirmpwd:
            return jsonify({"validation": "Re_confirm", "res": "Please Re-entery to confirm new password."})
        else:
            userid = current_user.get_id()
            check_pwd = database.get_user(userid, "password")
            if check_pwd[0] == oldpwd:
                database.update_user(userid, "password", newpwd)
                return jsonify({"validation": "Success"})
            else:
                return jsonify({"validation": "Wrong_pwd", "res": "Old password was wrong, enter again."})


@app.route('/updateProfile', methods=['GET', 'POST'])
def updateProfile():
    print(request.method)
    if request.method == 'POST':
        userid = current_user.get_id()
        print("hey")
        x = {}
        x['username'] = request.form['edit_username']
        x["name"] = request.form['edit_name']
        x["gender"] = request.form['edit_gender']
        x["birth"] = request.form['edit_birth']
        x["mobile"] = request.form['edit_mobile']
        x["address"] = request.form['edit_address']
        for key, value in x.items():
            database.update_user(userid, key, value)
    return render_template('profile.html', log="Log In")


@app.route('/profile')
def profile():
    return render_template('profile.html', log="Log In")


@app.route('/getUserData', methods=["GET", "POST"])
def getUserData():
    profile = {
        'userid': "1001 1001",
        'username': 'HELLO WORLD',
        'name': 'TONY CHEN',
        'gender': '0',
        'birth': '2019-02-20',
        'mobile': '2008 2008',
        'address': 'HKUST CLEAR WATER BAY'
    }
    print(profile)
    userid = current_user.get_id()
    print("id here: " + str(userid))
    if userid != None:
        sql = text("select * from User where id=" + str(userid))
        result = db.engine.execute(sql)
        db.session.commit()
        for row in result:
            print(row)
            profile['userid'] = row[0]
            profile['username'] = row[1]
            profile['name'] = row[2]
            # profile['password'] = row[3]
            profile['gender'] = row[4]
            profile['birth'] = row[5]
            profile['mobile'] = row[6]
            profile['address'] = row[7]
    return jsonify({'returnMSG': profile})


@app.route('/signup', methods=['GET', 'POST'])
def register():
    print(request.method)
    if request.method == 'POST':
        # render_template('register.html', log="Log IN")
        print("signup!!!")
        new_user = table.User(request.form['username'], request.form['name'], request.form['password1'],
                              request.form['gender'], request.form['birth'], request.form['phonenumber'],
                              request.form['address'], "not", "not", "0", 0, 0, False, datetime.datetime.now())
        print("sign up middle")
        db.session.add(new_user)
        db.session.commit()

        database.insert_employment(new_user.id)
        database.insert_divorce(new_user.id)

        sql = text("select * from employment")
        result = db.engine.execute(sql)
        db.session.commit()
        for row in result:
            print(row)

        print("sign up end!!!")
        return render_template("log_in.html")

    return render_template('register.html')


@app.route('/chat', methods=["GET", "POST"])
def chat():
    message = request.form["text"]
    widget = ""
    job_title = ""
    userid = current_user.get_id()

    print("userid: "+str(userid))

    if userid != None:
        goal = database.get_user_goal(userid)

        if goal.find("employment") != -1:
            state = database.get_user_state(userid)
            reply_message, widget, job_title = conversation.sequence_e(userid, state, message, nlp)
        elif goal.find("divorce") != -1:
            state = database.get_user_state(userid)
            reply_message, widget, job_title = conversation.sequence_d(userid, state, message, nlp)
        else:
            state = database.get_user(userid, "state")
            state = state[0]
            if state.find("not") != -1:
                database.update_user(userid, "state", "nnn")
                return jsonify({"status": "success", "response": "Hi What can we help you?", "state": state,"type": widget})
            reply_message = conversation.determine_goal(userid, message, nlp)

    else:
        ip = request.remote_addr

        sql = text("select * from User where username='" + ip + "'")
        result = db.engine.execute(sql)
        db.session.commit()
        x = []
        for row in result:
            x.append(row)
        if len(x) == 0:
            print("into new guest user!")
            new_user = User(str(request.remote_addr), "0", "0", "0", "0", "0", "0", "not", "not", "0", 0, 0, True,
                            datetime.datetime.now())
            db.session.add(new_user)
            db.session.commit()
            database.insert_employment(new_user.id)
            database.insert_divorce(new_user.id)

            userid = new_user.id
        else:
            userid = x[0][0]

        goal = database.get_user_goal(userid)

        if goal.find("employment") != -1:
            print("<-----chat employment----->")
            state = database.get_user_state(userid)
            reply_message, widget, job_title = conversation.sequence_e(userid, state, message, nlp)
        elif goal.find("divorce") != -1:
            state = database.get_user_state(userid)
            reply_message, widget, job_title = conversation.sequence_d(userid, state, message, nlp)
        else:
            state = database.get_user(userid, "state")
            state = state[0]
            if state.find("not") != -1:
                database.update_user(userid, "state", "nnn")
                return jsonify({"status": "success", "response": "Hi What can we help you?", "state": state, "type": ''})
            reply_message = conversation.determine_goal(userid, message, nlp)

    temp = reply_message + "|" + widget + "|" + job_title
    session["widget"] = temp

    return jsonify(
        {"status": "success", "response": reply_message, "state": state, "type": widget, "job_title": job_title})


@app.before_request
def before_request():
    print("into before_request")
    now = datetime.datetime.now()
    if current_user.get_id() == None:
        userid = database.get_user_id(str(request.remote_addr))
        database.update_user_last_modify(userid, now)
    else:
        userid = current_user.get_id()
        database.update_user_last_modify(userid, now)


@app.route('/testner', methods=['GET', 'POST'])
def testner():
    if request.method == 'POST':
        text = request.form['testner']
        name, location, organization = test_nlp.extract_entity(text)
        result = ''
        result += 'name: '
        for i in name:
            result = result + i + ', '
        result += '\n\nlocation: '
        for i in location:
            result = result + i + ', '
        result += '\n\norganization: '
        for i in organization:
            result = result + i + ', '
        return result
    return render_template("test_ner.html")


@app.route('/testspacy', methods=['GET', 'POST'])
def testspacy():
    if request.method == 'POST':
        text = request.form['testspacy']
        name, location, organization = test_nlp.extract_entity_spacy(text)
        result = ''
        result += 'name: '
        for i in name:
            result = result + str(i) + ', '
        result += '\n\n</br>location: '
        for i in location:
            result = result + str(i) + ', '
        result += '\n\n</br>organization: '
        for i in organization:
            result = result + str(i) + ', '
        return result

    return render_template("test_spacy.html")


@app.route('/testtextblob', methods=['GET', 'POST'])
def testtextblob():
    if request.method == 'POST':
        text = request.form['testtextblob']
        return "test textblob here!!!"

    return render_template("test_textblob.html")


@app.route('/hisdocs/<userid>')
def get_pdf(userid):
    num_temp1 = database.get_employ_column(userid, 'num_temp')
    num_temp2 = database.get_divorce_column(userid, 'num_temp')

    his_docs_employ = []
    his_docs_divorce = []

    for i in range(num_temp1):
        if i==0:
            doc = docs('Your 1st employment offer letter',"employment_pdf/employment_"+str(userid)+"_"+str(i+1)+".pdf",'1')
            his_docs_employ.append(doc)
        elif i==1:
            doc = docs('Your 2nd employment offer letter',"employment_pdf/employment_"+str(userid)+"_"+str(i+1)+".pdf",'2')
            his_docs_employ.append(doc)
        elif i==2:
            doc = docs('Your 3rd employment offer letter',"employment_pdf/employment_"+str(userid)+"_"+str(i+1)+".pdf",'3')
            his_docs_employ.append(doc)
        else:
            j = "Your "+str(i+1)+"th employment offer letter"
            doc = docs(j,"employment_pdf/employment_"+str(userid)+"_"+str(i+1)+".pdf",str(i+1))
            his_docs_employ.append(doc)

    for i in range(num_temp2):
        if i==0:
            doc = docs("Your 1st divorce contract", "divorce_pdf/divorce_"+str(userid)+"_"+str(i+1)+".pdf",'1')
            his_docs_divorce.append(doc)
        elif i==1:
            doc = docs("Your 2nd divorce contract", "divorce_pdf/divorce_"+str(userid)+"_"+str(i+1)+".pdf",'2')
            his_docs_divorce.append(doc)
        elif i==2:
            doc = docs("Your 3rd divorce contract", "divorce_pdf/divorce_"+str(userid)+"_"+str(i+1)+".pdf",'3')
            his_docs_divorce.append(doc)
        else:
            j = "Your "+str(i+1)+"th divorce contract"
            doc = docs(j, "divorce_pdf/divorce_"+str(userid)+"_"+str(i+1)+".pdf",str(i+1))
            his_docs_divorce.append(doc)
    
    print(his_docs_employ)
    print(his_docs_divorce)

    return render_template("docs.html",his_docs_employ=his_docs_employ, his_docs_divorce=his_docs_divorce)


@app.route('/employment/<userid>')
def get_employment(userid):
    num_temp = database.get_employ_column(userid, 'num_temp')
    file_name = "employment_" + str(userid) + "_" + str(num_temp) + ".pdf"
    directory = os.getcwd() + '/static/employment_pdf'
    try:
        return send_from_directory(directory, file_name, as_attachment=True)
    except:
        return "You have no employment template generated!"


@app.route('/employ_guest/<username>')
def get_employ_guest(username):
    userid = database.get_user_id(username)
    if userid != 0:
        num_temp = database.get_employ_column(userid, 'num_temp')
        file_name = "employment_" + str(userid) + "_" + str(num_temp) + ".pdf"
        directory = os.getcwd() + '/static/employment_pdf'
        try:
            return send_from_directory(directory, file_name, as_attachment=True)
        except:
            return "You have no employment template generated!"
    else:
        return "You have no employment template generated!"


@app.route('/divorce/<userid>')
def get_divorce(userid):
    userid = current_user.get_id()
    num_temp = database.get_divorce_column(userid, 'num_temp')
    file_name = "divorce_" + str(userid) + "_" + str(num_temp) + ".pdf"
    directory = os.getcwd() + '/static/divorce_pdf'
    try:
        return send_from_directory(directory, file_name, as_attachment=True)
    except:
        return "You have no divorce template generated!"


@app.route('/divorce_guest/<username>')
def get_divorce_guest(username):
    userid = database.get_user_id(username)
    if userid != 0:
        num_temp = database.get_divorce_column(userid, 'num_temp')
        file_name = "divorce_" + str(userid) + "_" + str(num_temp) + ".pdf"
        directory = os.getcwd() + '/static/divorce_pdf'
        try:
            return send_from_directory(directory, file_name, as_attachment=True)
        except:
            return "You have no divorce template generated!"
    else:
        return "You have no divorce template generated!"

def clear_expired():
    now = datetime.datetime.now()
    all_id = database.get_all_user_id()
    for userid in all_id:
        last_modify = database.get_user_last_modify(userid)
        delta = now - datetime.datetime.strptime(last_modify, '%Y-%m-%d %H:%M:%S.%f')
        print("into comparison")
        if delta > datetime.timedelta(seconds=EXPIRE_TIME):
            print("comparison successful")
            if database.get_user_guest(userid):
                print("try to delete guest user")
                database.delete_guest_user(userid)
            else:
                if database.get_user_state(userid) != "not":
                    print("try to delete user info")
                    database.clear_divorce(userid)
                    database.clear_employment(userid)

class docs:
    name = ''
    path = ''
    count = ''

    def __init__(self, name, path, count):
        self.name = name
        self.path = path
        self.count = count


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["DEBUG"] = True

nlp = spacy.load('en')

sql = text("select * from User")
result = db.engine.execute(sql)
db.session.commit()
for row in result:
    print(row)

sql = text("select * from employment")
result = db.engine.execute(sql)
db.session.commit()
for row in result:
    print(row)

sql = text("select * from divorce")
result = db.engine.execute(sql)
db.session.commit()
for row in result:
    print(row)
scheduler = BackgroundScheduler()
print("BackgroundScheduler start")
scheduler.add_job(clear_expired, 'interval', seconds=DATABASE_CLEAR_INTERVAL)
scheduler.start()

app.run(use_reloader=False)

