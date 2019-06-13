# standford NER

import user
# import chatbot
import datetime
from fpdf import FPDF
import database
import nltk
import nltk.downloader
from nltk.corpus import names
from spacy.tokens import Doc
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from spacy.lang.en.examples import sentences
import en_core_web_sm

import numpy as np
import pdf_employment
import pdf_divorce
import table
import webbrowser
from flask import send_file

response_all = ["Hi, what can I help you?\n",
                "Sorry, I can't understand what you want, please tell me what you want to do?\n",
                "here is the contract you want, please have a look. Do you want to modify something? (Y/N)\n",
                "Do you need more help?\n",
                "Bye, hope to see you again.\n"]

response_divorce = [
    "Could you tell me the name of wife?\n",
    "And the name of husband?\n",
    "Please input the HKID of wife? (Format:A111111(A))\n",
    "What's the address of wife?\n",
    "Please input the HKID of husband? (Format:A111111(A))\n",
    "What's the address of husband?\n",
    "What's wife's age?(please input a number)\n",
    "What's husband's age?(please input a number)\n",
    "What's your marriage date?\n",
    "How many children do you have?(please input a number)\n",
    "What's your children's name?(split by ;)\n",
    "What date are your children born?(split by ;)\n",
    "Who will adopt the children?(input father or mother and split by ;)\n",
    "Who will pay the children maintenance?(father or mother)\n",
    "who will pay the spousal maintenance?(husband or wife)\n",
    "How much will be the spousal maintenance per month?(input a number)\n",
    "How long will the spousal maintenance continue?(input a number whose unit is year)\n",
    "Please input the asset that will go to wife\n",
    "please input the asset that will go to husband\n"
]

response_employment = ["What's employee's name?(please input a name begin with capital letter)\n",
                       "What's employer's name?(please input a name begin with capital letter)\n",
                       "What's the company's name?(please input a name begin with capital letter)\n",
                       "What's the registered office address of the company?\n",
                       "What's the address of employee?\n",
                       "What's the job title?\n",
                       "What's the duty job?(split by ;)\n",
                       "Is the job full-time or part-time?\n",
                       "How many hours per week the employee required to work? (please input a number)",
                       "What's the monthly salary?(by HKD)\n",
                       "How many days of annual leave?\n",
                       "On what date will the employment commence?\n",
                       "What's the deadline of receive this letter?\n",
                       "Will the employee be required to work from a specific location or be allowed to work remotely or online?\n",
                       "What's the specific location that the employee will be expected to work?\n",
                       "Is there a probationary period?(Y/N)\n",
                       "What's the duration of the probationary period?(input a number whose unit is week)\n",
                       "How much advance notice is required for either party to terminate the employment?(input a number whose unit is week)\n",
                       "Will the employee be entitled to join the company's health insurance?(Y/N)\n",
                       "Will the employee be paid commission?(Y/N)\n"
                       ]

ordinal_number = {1: "st", 2: "nd", 3: "rd", 4: "th"}


def determine_type(input):
    try:
        x = int(input)
        return 1
    except:
        return 0


def determine_goal(userid, message, nlp):
    if (message.lower()).find("divorce") != -1 or (message.lower()).find("marry") != -1:
        emotion = determine_emotion(nlp, message)
        database.update_user_first_sentiment(userid, emotion)
        database.update_user(userid, "goal", "divorce")
        database.update_user(userid, "state", "0")
        if emotion > 0.2:
            return "I'm sorry about that but you have made a very courageous desicion! How do you feel now?"
        elif emotion < -0.2:
            return "Divorce is not always a bad thing, you don't need to worry that divorce is a bad thing. Indeed, you made a very courageous desicion! How do you feel now?"
        else:
            return "I'm sorry about that. How do you feel now?"
    elif (message.lower()).find("employ") != -1 or (message.lower()).find("labor") != -1 or (message.lower()).find(
            "labour") != -1 or (message.lower()).find("hire") != -1:
        database.update_user(userid, "goal", "employment")
        database.update_user(userid, "state", "0")
        return "You have already set a goal to be the employment letter! Input something to start!"
    else:
        print("test here")
        return "Sorry that we cannot find out what you want to do. Please input again."


def sequence_d(userid, state, message, nlp):
    print(state)

    widget = ""

    if state == 0:
        emotion = determine_emotion(nlp, message)
        second_sentiment = database.get_user_first_sentiment(userid)
        database.update_user_second_sentiment(userid, second_sentiment)
        database.update_user_first_sentiment(userid, emotion)
        database.update_user(userid, "state", str(1))
        emotion = emotion + second_sentiment
        if emotion > 0.2:
            return "Life is moving on, you are on your way. So let's get started. Could you tell me the wife's name?", "", ""
        elif emotion < -0.2:
            return """"Divorce isn't such a tragedy. A tragedy's staying in an unhappy marriage, teaching your children the wrong things about love. Nobody ever died of divorce." -Jennifer Weiner, Fly Away Home\n""" + """Whatever you are feeling is perfectly okay. Now, let's begin the contract, could you tell me the wife's name?""", "", ""
        else:
            return "Some people think that it's holding on that makes one strong; sometimes it's letting go. Don't worry about it so much, let's move on. Could you tell me the wife's name?", "", ""

    if str(state).find("child") != -1:
        num_child = int(database.get_divorce_column(userid, "num_child"))
        print("get into children part, num_child: " + str(num_child))
        child_state1 = int(state[6])
        child_state2 = int(state[8])
        if child_state1 < num_child:
            print("in child 1111 test")
            if child_state2 == 1:
                child_data = message.split(";")
                child_born = child_data[1]
                university = child_data[2]
                if university.find("0") != -1 or university.find("n") != -1:
                    university = "n"
                else:
                    university = "y"
                now = datetime.datetime.now()
                born_date = datetime.datetime.strptime(child_born, "%Y-%m-%d")
                delta = now - born_date
                age = delta.days / 365

                if child_state1 == 1:
                    database.update_divorce(userid, "child_name", child_data[0] + ";")
                    database.update_divorce(userid, "born_date", child_data[1] + ";")
                    database.update_divorce(userid, "university", university + ";")


                else:
                    child_exist_name = database.get_divorce_column(userid, "child_name")
                    child_exist_name = child_exist_name + child_data[0] + ";"
                    database.update_divorce(userid, "child_name", child_exist_name)
                    child_exist_born = database.get_divorce_column(userid, "born_date")
                    child_exist_born = child_exist_born + child_data[1] + ";"
                    database.update_divorce(userid, "born_date", child_exist_born)
                    university_child = database.get_divorce_column(userid, "university")
                    university_child = university_child + university + ";"
                    database.update_divorce(userid, "university", university_child)

                if age >= 18 and university == "n":
                    state = "child-" + str(child_state1 + 1) + ".1"
                    database.update_user(userid, "state", state)

                    if child_state1 == 1:
                        database.update_divorce(userid, "custody", ";")
                        database.update_divorce(userid, "major_charge", ";")
                        database.update_divorce(userid, "children_maintence", ";")
                        database.update_divorce(userid, "child_main_amount", ";")
                        database.update_divorce(userid, "child_main_who", ";")
                        database.update_divorce(userid, "child_main_modify", ";")
                        database.update_divorce(userid, "leave_hk", ";")
                        database.update_divorce(userid, "where_live", ";")
                        database.update_divorce(userid, "when_live", ";")
                        database.update_divorce(userid, "child_access", "|")


                    else:
                        x = database.get_divorce_column(userid, "custody")
                        x = x + ";"
                        database.update_divorce(userid, "custody", x)
                        x = database.get_divorce_column(userid, "major_charge")
                        x = x + ";"
                        database.update_divorce(userid, "major_charge", x)
                        x = database.get_divorce_column(userid, "child_access")
                        x = x + "|"
                        database.update_divorce(userid, "child_access", x)
                        x = database.get_divorce_column(userid, "children_maintence")
                        x = x + ";"
                        database.update_divorce(userid, "children_maintence", x)
                        x = database.get_divorce_column(userid, "child_main_amount")
                        x = x + ";"
                        database.update_divorce(userid, "child_main_amount", x)
                        x = database.get_divorce_column(userid, "child_main_who")
                        x = x + ";"
                        database.update_divorce(userid, "child_main_who", x)
                        x = database.get_divorce_column(userid, "child_main_modify")
                        x = x + ";"
                        database.update_divorce(userid, "child_main_modify", x)
                        x = database.get_divorce_column(userid, "leave_hk")
                        x = x + ";"
                        database.update_divorce(userid, "leave_hk", x)
                        x = database.get_divorce_column(userid, "where_live")
                        x = x + ";"
                        database.update_divorce(userid, "where_live", x)
                        x = database.get_divorce_column(userid, "when_live")
                        x = x + ";"
                        database.update_divorce(userid, "when_live", x)

                    widget = "child_info"
                    ordinal = ordinal_number.get(child_state1 + 1)
                    if not ordinal:
                        ordinal = 'th'
                    return "please enter some basic information of your " + str(
                        child_state1 + 1) + ordinal + " child", widget, ""
                else:
                    state = "child-" + str(child_state1) + ".2"
                    database.update_user(userid, "state", str(state))
                    widget = "child_main_info"
                    ordinal = ordinal_number.get(child_state1)
                    if not ordinal:
                        ordinal = 'th'
                    return "please enter some maintenance information of your " + str(
                        child_state1) + ordinal + " child", widget, ""

            elif child_state2 == 2:
                child_data = message.split(";")
                if child_state1 == 1:
                    database.update_divorce(userid, "children_maintence", child_data[0] + ";")
                    database.update_divorce(userid, "child_main_modify", child_data[1] + ";")
                    database.update_divorce(userid, "child_main_who", child_data[2] + ";")
                    database.update_divorce(userid, "child_main_amount", child_data[3] + ";")

                else:
                    x = database.get_divorce_column(userid, "children_maintence")
                    x = x + child_data[0] + ";"
                    database.update_divorce(userid, "children_maintence", x)
                    x = database.get_divorce_column(userid, "child_main_modify")
                    x = x + child_data[1] + ";"
                    database.update_divorce(userid, "child_main_modify", x)
                    x = database.get_divorce_column(userid, "child_main_who")
                    x = x + child_data[2] + ";"
                    database.update_divorce(userid, "child_main_who", x)
                    x = database.get_divorce_column(userid, "child_main_amount")
                    x = x + child_data[3] + ";"
                    database.update_divorce(userid, "child_main_amount", x)

                birth = database.get_divorce_column(userid, "born_date")
                print(birth)
                birth = birth.split(";")
                birth = birth[child_state1 - 1]
                now = datetime.datetime.now()
                born_date = datetime.datetime.strptime(birth, "%Y-%m-%d")
                delta = now - born_date
                age = delta.days / 365

                if age >= 18:
                    if child_state1 == 1:
                        database.update_divorce(userid, "custody", ";")
                        database.update_divorce(userid, "major_charge", ";")
                        database.update_divorce(userid, "child_access", "|")
                        database.update_divorce(userid, "leave_hk", ";")
                        database.update_divorce(userid, "where_live", ";")
                        database.update_divorce(userid, "when_live", ";")
                    else:
                        x = database.get_divorce_column(userid, "custody")
                        x = x + ";"
                        database.update_divorce(userid, "custody", x)
                        x = database.get_divorce_column(userid, "major_charge")
                        x = x + ";"
                        database.update_divorce(userid, "major_charge", x)
                        x = database.get_divorce_column(userid, "child_access")
                        x = x + "|"
                        database.update_divorce(userid, "child_access", x)
                        x = database.get_divorce_column(userid, "leave_hk")
                        x = x + ";"
                        database.update_divorce(userid, "leave_hk", x)
                        x = database.get_divorce_column(userid, "where_live")
                        x = x + ";"
                        database.update_divorce(userid, "where_live", x)
                        x = database.get_divorce_column(userid, "when_live")
                        x = x + ";"
                        database.update_divorce(userid, "when_live", x)

                    state = "child-" + str(child_state1 + 1) + ".1"
                    database.update_user(userid, "state", str(state))
                    widget = "child_info"
                    ordinal = ordinal_number.get(child_state1 + 1)
                    if not ordinal:
                        ordinal = 'th'
                    return "Please enter some basic information of your " + str(
                        child_state1 + 1) + ordinal + " child.", widget, ""
                else:
                    state = "child-" + str(child_state1) + ".3"
                    database.update_user(userid, "state", str(state))
                    widget = "child_further_info"
                    ordinal = ordinal_number.get(child_state1)
                    if not ordinal:
                        ordinal = 'th'
                    return "Please enter some further information of your " + str(
                        child_state1) + ordinal + " child.", widget, ""
            elif child_state2 == 3:
                child_data = message.split(";")
                if child_state1 == 1:
                    database.update_divorce(userid, "custody", child_data[0] + ";")
                    database.update_divorce(userid, "major_charge", child_data[1] + ";")
                    database.update_divorce(userid, "leave_hk", child_data[2] + ";")
                    database.update_divorce(userid, "where_live", child_data[3] + ";")
                    database.update_divorce(userid, "when_live", child_data[4] + ";")

                else:
                    x = database.get_divorce_column(userid, "custody")
                    x = x + child_data[0] + ";"
                    database.update_divorce(userid, "custody", x)
                    x = database.get_divorce_column(userid, "major_charge")
                    x = x + child_data[1] + ";"
                    database.update_divorce(userid, "major_charge", x)
                    x = database.get_divorce_column(userid, "leave_hk")
                    x = x + child_data[2] + ";"
                    database.update_divorce(userid, "leave_hk", x)
                    x = database.get_divorce_column(userid, "where_live")
                    x = x + child_data[3] + ";"
                    database.update_divorce(userid, "where_live", x)
                    x = database.get_divorce_column(userid, "when_live")
                    x = x + child_data[4] + ";"
                    database.update_divorce(userid, "when_live", x)

                state = "child-" + str(child_state1) + ".4"
                database.update_user(userid, "state", str(state))
                widget = "asset"
                ordinal = ordinal_number.get(child_state1)
                if not ordinal:
                    ordinal = 'th'
                return "Please enter access information of your " + str(child_state1) + ordinal + " child.", widget, ""
            else:
                child_data = message
                if child_state1 == 1:
                    database.update_divorce(userid, "child_access", child_data + "|")
                else:
                    x = database.get_divorce_column(userid, "child_access")
                    x = x + child_data + "|"
                    database.update_divorce(userid, "child_access", x)

                state = "child-" + str(child_state1 + 1) + ".1"
                database.update_user(userid, "state", str(state))
                widget = "child_info"
                ordinal = ordinal_number.get(child_state1 + 1)
                if not ordinal:
                    ordinal = 'th'
                return "Please enter basic information of your " + str(
                    child_state1 + 1) + ordinal + " child.", widget, ""

        else:
            child_data = message.split(";")
            if child_state2 == 1:
                child_born = child_data[1]
                now = datetime.datetime.now()
                born_date = datetime.datetime.strptime(child_born, "%Y-%m-%d")
                delta = now - born_date
                age = delta.days / 365
                university = child_data[2]
                if university.find("0") != -1 or university.find("n") != -1:
                    university = "n"
                else:
                    university = "y"

                if child_state1 == 1:
                    database.update_divorce(userid, "child_name", child_data[0])
                    database.update_divorce(userid, "born_date", child_data[1])
                    database.update_divorce(userid, "university", university)


                else:
                    child_exist_name = database.get_divorce_column(userid, "child_name")
                    child_exist_name = child_exist_name + child_data[0]
                    database.update_divorce(userid, "child_name", child_exist_name)
                    child_exist_born = database.get_divorce_column(userid, "born_date")
                    child_exist_born = child_exist_born + child_data[1]
                    database.update_divorce(userid, "born_date", child_exist_born)
                    university_child = database.get_divorce_column(userid, "university")
                    university_child = university_child + university
                    database.update_divorce(userid, "university", university_child)

                if age >= 18 and university == "n":
                    state = 14
                    widget = "couple"
                    database.update_user(userid, "state", str(state))

                    if child_state1 == 1:
                        database.update_divorce(userid, "custody", "")
                        database.update_divorce(userid, "major_charge", "")
                        database.update_divorce(userid, "child_access", "")
                        database.update_divorce(userid, "children_maintence", "")
                        database.update_divorce(userid, "child_main_amount", "")
                        database.update_divorce(userid, "child_main_who", "")
                        database.update_divorce(userid, "child_main_modify", "")
                        database.update_divorce(userid, "leave_hk", "")
                        database.update_divorce(userid, "where_live", "")
                        database.update_divorce(userid, "when_live", "")


                else:
                    state = "child-" + str(child_state1) + ".2"
                    database.update_user(userid, "state", str(state))
                    widget = "child_main_info"
                    ordinal = ordinal_number.get(child_state1)
                    if not ordinal:
                        ordinal = 'th'
                    return "please enter some maintenance information of your " + str(
                        child_state1) + ordinal + " child", widget, ""


            elif child_state2 == 2:
                child_data = message.split(";")
                if child_state1 == 1:
                    database.update_divorce(userid, "children_maintence", child_data[0])
                    database.update_divorce(userid, "child_main_modify", child_data[1])
                    database.update_divorce(userid, "child_main_who", child_data[2])
                    database.update_divorce(userid, "child_main_amount", child_data[3])

                else:
                    x = database.get_divorce_column(userid, "children_maintence")
                    x = x + child_data[0]
                    database.update_divorce(userid, "children_maintence", x)
                    x = database.get_divorce_column(userid, "child_main_modify")
                    x = x + child_data[1]
                    database.update_divorce(userid, "child_main_modify", x)
                    x = database.get_divorce_column(userid, "child_main_who")
                    x = x + child_data[2]
                    database.update_divorce(userid, "child_main_who", x)
                    x = database.get_divorce_column(userid, "child_main_amount")
                    x = x + child_data[3]
                    database.update_divorce(userid, "child_main_amount", x)

                birth = database.get_divorce_column(userid, "born_date")
                birth = birth.split(";")
                birth = birth[child_state1 - 1]
                now = datetime.datetime.now()
                born_date = datetime.datetime.strptime(birth, "%Y-%m-%d")
                delta = now - born_date
                age = delta.days / 365

                if age >= 18:
                    if child_state1 == 1:
                        database.update_divorce(userid, "custody", "")
                        database.update_divorce(userid, "major_charge", "")
                        database.update_divorce(userid, "child_access", "")
                        database.update_divorce(userid, "leave_hk", "")
                        database.update_divorce(userid, "where_live", "")
                        database.update_divorce(userid, "when_live", "")

                    state = 14
                    database.update_user(userid, "state", str(state))
                    widget = "couple"

                else:
                    state = "child-" + str(child_state1) + ".3"
                    database.update_user(userid, "state", str(state))
                    widget = "child_further_info"
                    ordinal = ordinal_number.get(child_state1)
                    if not ordinal:
                        ordinal = 'th'
                    return "Please enter some further information of your " + str(
                        child_state1) + ordinal + " child.", widget, ""

            elif child_state2 == 3:
                child_data = message.split(";")
                if child_state1 == 1:
                    database.update_divorce(userid, "custody", child_data[0])
                    database.update_divorce(userid, "major_charge", child_data[1])
                    database.update_divorce(userid, "leave_hk", child_data[2])
                    database.update_divorce(userid, "where_live", child_data[3])
                    database.update_divorce(userid, "when_live", child_data[4])

                else:
                    x = database.get_divorce_column(userid, "custody")
                    x = x + child_data[0]
                    database.update_divorce(userid, "custody", x)
                    x = database.get_divorce_column(userid, "major_charge")
                    x = x + child_data[1]
                    database.update_divorce(userid, "major_charge", x)
                    x = database.get_divorce_column(userid, "leave_hk")
                    x = x + child_data[2]
                    database.update_divorce(userid, "leave_hk", x)
                    x = database.get_divorce_column(userid, "where_live")
                    x = x + child_data[3]
                    database.update_divorce(userid, "where_live", x)
                    x = database.get_divorce_column(userid, "when_live")
                    x = x + child_data[4]
                    database.update_divorce(userid, "when_live", x)

                state = "child-" + str(child_state1) + ".4"
                database.update_user(userid, "state", str(state))
                widget = "asset"
                ordinal = ordinal_number.get(child_state1)
                if not ordinal:
                    ordinal = 'th'
                return "Please enter access information of your " + str(child_state1) + ordinal + " child.", widget, ""

            else:
                child_data = message
                if child_state1 == 1:
                    database.update_divorce(userid, "child_access", child_data)
                else:
                    x = database.get_divorce_column(userid, "child_access")
                    x = x + child_data
                    database.update_divorce(userid, "child_access", x)

                state = 14
                database.update_user(userid, "state", str(state))
                widget = "couple"

    if state == 1 or state == 2:
        name = extract_name_spacy(nlp, message)
        if len(name) == 0:
            # select from name db here and check whether it exist or not
            if not database.exist_name(message):
                reply_message = "Sorry, we cannot find a name from your response here. Please choose to update our database or enter another one again."
                widget = "name_update"
                database.update_user(userid, "state", str(state) + ".1")
                return reply_message, widget, ""
        else:
            message = str(name[0])

    if str(state).find("1.1") != -1:
        message = message.split(";")
        if message[1].find("update") != -1:
            database.insert_name(message[0])
            state = 1
            message = message[0]
            print("test update name db")
        else:
            name = extract_name_spacy(nlp, message[0])
            if len(name) == 0:
                if not database.exist_name(message[0]):
                    reply_message = "Sorry, we cannot find a name from your response here. Please choose to update our database or enter another one again."
                    widget = "name_update"
                    return reply_message, widget, ""
                else:
                    state = 1
                    widget = ""
                    message = message[0]
            else:
                state = 1
                widget = ""
                message = str(name[0])

    if str(state).find("2.1") != -1:
        message = message.split(";")
        if message[1].find("update") != -1:
            # update name db here
            database.insert_name(message[0])
            state = 2
            message = message[0]
            print("test update name db")
        else:
            name = extract_name_spacy(nlp, message[0])
            if len(name) == 0:
                if not database.exist_name(message[0]):
                    reply_message = "Sorry, we cannot find a name from your response here. Please choose to update our database or enter another one again."
                    widget = "name_update"
                    return reply_message, widget, ""
                else:
                    state = 2
                    widget = ""
                    message = message[0]
            else:
                state = 2
                widget = ""
                message = str(name[0])

    if state == 3 or state == 5:
        hkid = extract_hkid(message)
        if hkid.find('n') != -1:
            reply_message = "Please input a correct HKID number!"
            return reply_message, "", ""
        message = hkid

    # number input type
    if state == 7 or state == 8 or state == 10 or state == 16 or state == 17:
        if determine_type(message) == 0:
            reply_message = "Error input type! please input a number!"
            return reply_message, widget, ""

    if state == 11 or state == 12 or state == 13 or state == 18 or state == 19:
        temp = message.split(";")

    if state == 10:
        if int(message) == 0:
            state = 14
            database.update_divorce(userid, "custody", "n")
            database.update_divorce(userid, "born_date", "n")
            database.update_divorce(userid, "child_name", "n")
            database.update_divorce(userid, "children_maintence", "n")
            database.update_divorce(userid, "child_access", "n")
            database.update_divorce(userid, "child_main_amount", "n")
            database.update_divorce(userid, "major_charge", "n")
            database.update_divorce(userid, "leave_hk", "n")
            database.update_divorce(userid, "where_live", "n")
            database.update_divorce(userid, "when_live", "n")
            database.update_divorce(userid, "child_main_modify", "n")
            database.update_divorce(userid, "child_main_who", "n")
            database.update_divorce(userid, "university", "n")

            widget = "couple"
        else:
            database.update_divorce_info(userid, state, message)
            state = "child-1.1"
            database.update_user(userid, "state", str(state))
            widget = "child_info"
            return "Please enter some basic information of your 1st child.", widget, ""

    if state <= 18:
        reply_message = response_divorce[state]

    if state == 20:
        if message.find("n") != -1 or message.find("N") != -1:
            reply_message = "Thanks! You have already finish your divorce contract!"
            num_temp = database.get_divorce_column(userid, 'num_temp')
            database.update_user(userid, "state", "999")
            return reply_message, widget, ""
        else:
            reply_message = "What do you want to modify?(please input a number)\n" + "1. mother's name\n" + "2. father's name\n" + "3. mother's hkid\n" + "4. mother's address\n" + "5. father's hkid\n" + "6. father's address\n" + "7. mother's age\n" + "8. father's age\n" + "9. marriage date\n"
            database.update_user(userid, "state", "100")
            return reply_message, widget, ""

    if state == 100:
        if determine_type(message) == 0:
            reply_message = "Error input type! please input a number!"
            return reply_message, widget, ""
        else:
            reply_message = "Please input the information that you want to replace the original one."
            print("message: " + message)
            database.update_user(userid, "modify", message)
            database.update_user(userid, "state", "200")
            widget = determine_modify(message)
            return reply_message, widget, ""

    if state == 200:
        x = database.get_user(userid, "modify")
        x = int(x[0])
        if x == 1 or x == 2:
            name = extract_name_spacy(nlp, message)
            if len(name) > 0:
                database.update_divorce_info(userid, x, str(name[0]))
            else:
                return "we cannot recognize the name from your input, please input again.", "", ""
        if x == 3 or x == 5:
            if not check_hkid(message):
                return "Please input a correct format of HKID, thanks.", "", ""

        database.modify_divorce(userid, x, message)
        print("test here !!!state 200")
        reply_message = "Already modify? anything else?(y/n)"
        database.update_user(userid, "state", "21")
        return reply_message, widget, ""

    if state == 21:
        if message.find("n") != -1 or message.find("N") != -1:
            emotion1 = database.get_user_first_sentiment(userid)
            emotion2 = database.get_user_second_sentiment(userid)
            emotion = emotion1 + emotion2
            if emotion > 0.2:
                reply_message = "Welcome to your new life, and you have finish your divorce contract! You can download it though the 'download divorce pdf' button or find it later in your personal profile."
            elif emotion < -0.2:
                reply_message = "What does not kill you makes you stronger. It's time to move on and enjoy your new life. This is the end of the process, and you can download the contract though the 'download divorce pdf' button or find it later in your personal profile."
            else:
                reply_message = "This is the end of the process. I hope you could move on and enjoy your new life. You can download the contract though the 'download divorce pdf' button or find it later in your personal profile."

            database.update_user(userid, "state", "999")
            info = database.get_divorce(userid)
            print(info)
            num_temp = database.get_divorce_column(userid, 'num_temp')
            pdf_divorce.generate_pdf_divorce(info, userid, num_temp)

            return reply_message, widget, ""

        else:
            reply_message = "What do you want to modify?(please input a number)\n" + "1. mother's name\n" + "2. father's name\n" + "3. mother's hkid\n" + "4. mother's address\n" + "5. father's hkid\n" + "6. father's address\n" + "7. mother's age\n" + "8. father's age\n" + "9. marriage date\n"
            database.update_user(userid, "state", "100")
            return reply_message, widget, ""

    if state == 999:
        if message.find("restart") != -1:
            database.update_user(userid, "state", "not")
            database.update_user(userid, "goal", "not")
            reply_message = "Hi, Here we start it again~"
            num_temp = database.get_divorce_column(userid, 'num_temp')
            database.update_divorce(userid, 'num_temp', num_temp + 1)
            database.clear_divorce(userid)
        else:
            reply_message = "You have already finished the letter! If you want to start it again, please input 'restart'."
        return reply_message, widget, ""

    if state == 15:
        spousal_main = message.split(";")
        database.update_divorce(userid, "spousal_maintance", spousal_main[0])
        database.update_divorce(userid, "spousal_who", spousal_main[1])
        database.update_divorce(userid, "spousal_type", spousal_main[2])
        database.update_divorce(userid, "spousal_much", spousal_main[3])
        database.update_user(userid, "state", str(18))
        widget = "asset"
        reply_message = response_divorce[17]
        return reply_message, widget, ""

    database.update_divorce_info(userid, state, message)
    print("state: " + str(state))
    # connect to user db and update user's state
    database.update_user(userid, "state", str(state + 1))

    if state == 19:
        info = database.get_divorce(userid)
        print(info)

        num_temp = database.get_divorce_column(userid, 'num_temp')
        pdf_divorce.generate_pdf_divorce(info, userid, num_temp)

        reply_message = "Now you can download the pdf file, please have a look \n" + "Do you want to modify something?(y/n)"

    if state == 8:
        print("into calendar!!!!!")
        widget = "calendar"

    if state == 14:
        widget = "spousal"
        reply_message = "please into some information about spousal maintenance"

    if state == 5 or state == 3:
        print("into state address here!!!")
        widget = "address"

    if state == 17 or state == 18:
        widget = "asset"

    return reply_message, widget, ""


def sequence_e(userid, state, message, nlp):
    print("employment! state: " + str(state))
    widget = ""

    if state == 0:
        database.update_user(userid, "state", str(state + 1))
        return "Let's start our employment offer letter, could you tell me the name of employee?", "", ""

    ####using Standford NER to extract person name here
    if state == 1 or state == 2:
        name = extract_name_spacy(nlp, message)
        if len(name) == 0:
            # select from name db here and check whether it exist or not
            if not database.exist_name(message):
                reply_message = "Sorry, we cannot find a name from your response here. Please choose to update our database or enter another one again."
                widget = "name_update"
                database.update_user(userid, "state", str(state) + ".1")
                return reply_message, widget, ""
        else:
            message = str(name[0])

    if str(state).find("1.1") != -1:
        message = message.split(";")
        if message[1].find("update") != -1:
            database.insert_name(message[0])
            state = 1
            message = message[0]
            print("test update name db")
        else:
            name = extract_name_spacy(nlp, message[0])
            if len(name) == 0:
                if not database.exist_name(message[0]):
                    reply_message = "Sorry, we cannot find a name from your response here. Please choose to update our database or enter another one again."
                    widget = "name_update"
                    return reply_message, widget, ""
                else:
                    state = 1
                    widget = ""
                    message = message[0]
            else:
                state = 1
                widget = ""
                message = str(name[0])

    if str(state).find("2.1") != -1:
        message = message.split(";")
        if message[1].find("update") != -1:
            # update name db here
            database.insert_name(message[0])
            state = 2
            message = message[0]
            print("test update name db")
        else:
            name = extract_name_spacy(nlp, message[0])
            if len(name) == 0:
                if not database.exist_name(message[0]):
                    reply_message = "Sorry, we cannot find a name from your response here. Please choose to update our database or enter another one again."
                    widget = "name_update"
                    return reply_message, widget, ""
                else:
                    state = 2
                    widget = ""
                    message = message[0]
            else:
                state = 2
                widget = ""
                message = str(name[0])

    if state == 3:
        organization = extract_organization_spacy(nlp, message)
        if len(organization) == 0:
            if not database.exist_organization(message):
                reply_message = "Sorry, we cannot find the company name from your response here. Please choose to update our database or enter another one again."
                widget = "name_update"
                database.update_user(userid, "state", str(state) + ".1")
                return reply_message, widget, ""
        else:
            message = str(organization[0])

    if str(state).find("3.1") != -1:
        message = message.split(";")
        if message[1].find("update") != -1:
            database.insert_organization(message[0])
            state = 3
            widget = "address"
            message = message[0]
            print("test update organization db")
        else:
            organization = extract_organization_spacy(nlp, message[0])
            if len(organization) == 0:
                if not database.exist_organization(message[0]):
                    reply_message = "Sorry, we cannot find the company name from your response here. Please choose to update our database or enter another one again."
                    widget = "name_update"
                    return reply_message, widget, ""
                else:
                    state = 3
                    widget = "address"
                    message = message[0]
            else:
                state = 3
                widget = "address"
                message = str(organization[0])

    if state == 6:
        widget = ""
        count, job = noun_chunks_spacy(nlp, message)
        if count == 0:
            reply_message = "We cannot recognize job title from your input, please input again!"
            return reply_message, widget, ""
        elif count == 1:
            message = job
            widget = "asset"
        else:
            # add wigdet here
            widget = "job"
            reply_message = "We cannot recognize what's your job title from your input, please choose one from the following:"
            job_title = job[0]
            for i in range(1, count):
                job_title = job_title + ";" + job[i]
            return reply_message, widget, job_title

    # full time or part time
    if state == 8:
        full = message.split(";")
        if full[0].find("full") != -1:
            database.update_employment(userid, "full", "full")
        else:
            database.update_employment(userid, "full", "part")
            database.update_employment(userid, "work_hour", full[1])
        database.update_user(userid, "state", "10")
        return response_employment[9], "", ""

    # number
    if state == 9 or state == 10 or state == 11 or state == 17 or state == 18:
        if determine_type(message) == 0:
            reply_message = "Error input type! please input a number!"
            return reply_message, "", ""
    if state == 10:
        salary = float(message)
        full = database.get_employ_column(userid, "full")
        if str(full).find("full") != -1:
            if salary < 6900:
                reply_message = "We find that the month salary here is lower than the minimum wage in HK. Please ensure your input, and if you want to modify it, please do in at the end of the conversation.\n Please input the annual leave."
                database.update_employment_info(userid, state, message)
                database.update_user(userid, "state", str(state + 1))
                return reply_message, "", ""
        else:
            work_hour = database.get_employ_column(userid, "work_hour")
            work_hour = int(work_hour)
            if salary / (work_hour * 4) < 37.5:
                reply_message = "We find that the month salary here is lower than the minimum wage in HK. Please ensure your input, and if you want to modify it, please do in at the end of the conversation.\n Please input the annual leave."
                database.update_employment_info(userid, state, message)
                database.update_user(userid, "state", str(state + 1))
                return reply_message, "", ""

    # y/n
    if state == 19 or state == 20:
        temp = determine_y_n(nlp, message)
        if temp == 1:
            message = "y"
        elif temp == -1:
            message = "n"
        else:
            reply_message = "We cannot recognize the answer from your input, please input again!"
            return reply_message, "", ""

    if state <= 19:
        # specific have another question
        if state == 14:
            remote = message.split(";")
            if remote[0].find("remote") != -1:
                database.update_employment(userid, "remote", "remote")
            else:
                database.update_employment(userid, "remote", "specific")
                database.update_employment(userid, "work_place", remote[1])
            database.update_user(userid, "state", "16")
            return response_employment[15], "probationary", ""

        if state == 16:
            probationary = message.split(";")
            if probationary[0].find("n") != -1 or probationary[0].find("N") != -1:
                database.update_employment(userid, "probationary", "n")
            else:
                database.update_employment(userid, "probationary", "y")
                database.update_employment(userid, "duration", probationary[1])
            database.update_user(userid, "state", "18")
            return response_employment[17], "", ""

        reply_message = response_employment[state]

    elif state == 21:
        if message.find("n") != -1 or message.find("N") != -1:
            reply_message = "Thanks! You have already finish your employment letter!"
            database.update_user(userid, "state", "999")
            num_temp = database.get_employ_column(userid, 'num_temp')
            return reply_message, widget, ""
        else:
            reply_message = "What do you want to modify?(please input a number)\n" + "1. employee's name\n" + "2. employer's name\n" + "3. company name\n" + "4. company address\n" + "5. employee address\n" + "6. job\n" + "7. duty\n" + "8. full-time or part-time\n" + "9. salary\n" + "10. annual leave\n" + "11. commence date\n" + "12. deadline of accept the letter\n" + "13. remote or specific place\n" + "14. probationary or not\n" + "15. advance week of terminate employment\n" + "16. health insurance or not\n" + "17. commission or not"
            database.update_user(userid, "state", "100")
            return reply_message, widget, ""

    if state == 999:
        if message.find("restart") != -1:
            database.update_user(userid, "state", "not")
            database.update_user(userid, "goal", "not")
            num_temp = database.get_employ_column(userid, 'num_temp')
            database.update_employment(userid, 'num_temp', num_temp + 1)
            database.clear_employment(userid)
            reply_message = "Hi, Here we start it again~"
        else:
            reply_message = "You have already finished the letter! If you want to start it again, please input 'restart'."
        return reply_message, widget, ""

    elif state == 100:
        if determine_type(message) == 0:
            reply_message = "Error input type! please input a number!"
            return reply_message
        else:
            reply_message = "Please input the message which you want to replace the original one."
            print("message: " + message)
            database.update_user(userid, "modify", message)
            database.update_user(userid, "state", "200")
            widget = employ_modify(message)
            return reply_message, widget, ""

    elif state == 200:
        x = database.get_user(userid, "modify")
        x = int(x[0])
        if x == 1 or x == 2:
            name = extract_name_spacy(nlp, message)
            if len(name) > 0:
                message = str(name[0])
            else:
                return "Please input a correct name!", "", ""
        elif x == 3:
            name = extract_organization_spacy(nlp, message)
            if len(name) > 0:
                message = str(name[0])
            else:
                return "Please input a correct organization name!", "", ""
        elif x == 6:
            length, name = noun_chunks_spacy(nlp, message)
            if length != 1:
                return "Sorry we cannot recognize the job title from your input, please input again", "", ""
            else:
                message = str(name[0])
        elif x == 9 or x == 10 or x == 15:
            if determine_type(message) == 0:
                return "Error input type, please input a number here", "", ""
        elif x == 16 or x == 18:
            y = determine_y_n(nlp, message)
            if y > 0:
                message = 'n'
            elif y < 0:
                message = 'y'
            else:
                return "We cannot recognize your input, please input again", "", ""
        elif x == 8:
            full = message.split(";")
            if full[0].find("full") != -1:
                database.update_employment(userid, "full", "full")
            else:
                database.update_employment(userid, "full", "part")
                database.update_employment(userid, "work_hour", full[1])
            reply_message = "Already modify? anything else?(y/n)"
            database.update_user(userid, "state", "22")
            return reply_message, "", ""
        elif x == 13:
            remote = message.split(";")
            if remote[0].find("remote") != -1:
                database.update_employment(userid, "remote", "remote")
            else:
                database.update_employment(userid, "remote", "specific")
                database.update_employment(userid, "work_place", remote[1])
            database.update_user(userid, "state", "22")
            reply_message = "Already modify? anything else?(y/n)"
            return reply_message, "", ""

        elif x == 14:
            probationary = message.split(";")
            if probationary[0].find("n") != -1 or probationary[0].find("N") != -1:
                database.update_employment(userid, "probationary", "n")
            else:
                database.update_employment(userid, "probationary", "y")
                database.update_employment(userid, "duration", probationary[1])
            database.update_user(userid, "state", "22")
            reply_message = "Already modify? anything else?(y/n)"
            return reply_message, "", ""

        database.modify_employment(userid, x, message)
        print("test here !!!state 200")
        reply_message = "Already modify? anything else?(y/n)"
        database.update_user(userid, "state", "22")
        return reply_message, widget, ""

    elif state == 22:
        if message.find("n") != -1 or message.find("N") != -1:
            reply_message = "Thanks! You have already finish your employment letter! Please download it by pressing the 'download employment pdf' botton"
            database.update_user(userid, "state", "999")
            info = database.get_employment(userid)
            num_temp = database.get_employ_column(userid, 'num_temp')

            if info[13].find("remote") != -1:
                info[13] = 0
                info[14] = 0
            else:
                info[13] = 1

            if info[15].find('n') != -1 or info[15].find("N") != -1:
                info[15] = 0
                info[16] = 0
            else:
                info[15] = 1

            if info[18].find('n') != -1 or info[18].find("N") != -1:
                info[18] = 0
            else:
                info[18] = 1

            if info[19].find('n') != -1 or info[19].find("N") != -1:
                info[19] = 0
            else:
                info[19] = 1

            num_temp = database.get_employ_column(userid, 'num_temp')
            pdf_employment.generate_pdf_employment(info, userid, num_temp)
            return reply_message, widget, ""

        else:
            reply_message = "What do you want to modify?(please input a number)\n" + "1. employee's name\n" + "2. employer's name\n" + "3. company name\n" + "4. company address\n" + "5. employee address\n" + "6. job\n" + "7. duty\n" + "8. full-time or part-time\n" + "9. salary\n" + "10. annual leave\n" + "11. commence date\n" + "12. deadline of accept the letter\n" + "13. remote or specific place\n" + "14. probationary or not\n" + "15. advance week of terminate employment\n" + "16. health insurance or not\n" + "17. commission or not"
            database.update_user(userid, "state", "100")
            return reply_message, widget, ""

    # connect to employment db! write info into it!
    database.update_employment_info(userid, state, message)

    print("state: " + str(state))

    # connect to user db and update user's state
    database.update_user(userid, "state", str(state + 1))

    if state == 20:
        # connect to employment db ! get all the info and store them into an array!
        # postprocess some info here!
        info = database.get_employment(userid)

        if info[13].find("remote") != -1:
            info[13] = 0
            info[14] = 0
        else:
            info[13] = 1

        if info[15].find('n') != -1 or info[15].find("N") != -1:
            info[15] = 0
            info[16] = 0
        else:
            info[15] = 1

        if info[18].find('n') != -1 or info[18].find("N") != -1:
            info[18] = 0
        else:
            info[18] = 1

        if info[19].find('n') != -1 or info[19].find("N") != -1:
            info[19] = 0
        else:
            info[19] = 1

        print(info)
        num_temp = database.get_employ_column(userid, 'num_temp')
        pdf_employment.generate_pdf_employment(info, userid, num_temp)

        reply_message = "Now you can download the pdf file, please have a look \n" + "Do you want to modify something?(y/n)\n" + "And also please ensure that employee is older than 13 years-old to make this employment legal."

    if state == 11 or state == 12:
        widget = "calendar"

    # if state==15 or state==18 or state==19:
    # 	widget = "yes_or_no"

    if state == 6:
        widget = "asset"

    if state == 7:
        widget = "full_part"

    if state == 13:
        widget = "remote_specific"

    if state == 3 or state == 4 or state == 14:
        widget = "address"

    return reply_message, widget, ""


def extract_hkid(text):
    for i in [',', '.', ';', ':', '!', '~', '?']:
        text = text.replace(i, '')
    text = text.split()

    if len(text) == 1:
        if len(text[0]) == 10:
            if check_hkid(text[0]):
                return text[0]
            return 'n'
        return 'n'

    s1 = []
    for i in range(len(text)):
        x = []
        x.append(text[i])
        s1.append(x)

    s3 = [nltk.pos_tag(sent) for sent in s1]
    s3 = np.array(s3)

    print(s3)

    # find the word behind 'is'
    result = np.where(s3 == 'VBZ')

    print(s3[result[0][0] + 1][0][0])
    if check_hkid(s3[result[0][0] + 1][0][0]):
        return s3[result[0][0] + 1][0][0]
    return 'n'


def check_hkid(text):
    if text[0].isupper() and text[1:7].isdigit() and text[7].find('(') != -1 and text[9].find(')') != -1:
        if text[8].isdigit() or text[8].isupper():
            return True
    return False


def cleanup(token, lower=True):
    if lower:
        token = token.lower()
    return token.strip()


def extract_name_spacy(nlp, text):
    # nlp = spacy.load('en')
    doc = nlp(text.encode('utf8').decode('utf8'))

    if len(doc) == 1:
        text = "The person name is " + text
        doc = nlp(text.encode('utf8').decode('utf8'))

    name = []

    for e in doc.ents:
        if e.label_ == u'PERSON':
            name.append(e)

    return name


def extract_organization_spacy(nlp, text):
    doc = nlp(text.encode('utf8').decode('utf8'))

    if len(doc) == 1:
        text = "The company name is " + text
        doc = nlp(text.encode('utf8').decode('utf8'))

    organization = []

    for e in doc.ents:
        if e.label_ == u'ORG':
            organization.append(e)

    return organization


def extract_location_spacy(nlp, text):
    doc = nlp(text.encode('utf8').decode('utf8'))

    location = ''

    for e in doc.ents:
        if e.label_ == u'GPE':
            if location == '':
                location = e
            else:
                location = location + ', ' + e

    return location


def noun_chunks_spacy(nlp, text):
    doc = nlp(text.encode('utf8').decode('utf8'))

    result = []

    for chunk in doc.noun_chunks:
        doc2 = nlp(chunk.text)
        incorrect = False
        for i in doc2:
            if i.tag_ == 'PRP$' or i.pos_ == 'PRON' or i.pos_ == 'PROPN':
                incorrect = True
        if not incorrect:
            result.append(str(chunk.text))

    if len(result) == 0:
        return 0, result

    elif len(result) == 1:
        return 1, result[0]

    else:
        for i in result:
            if i.find("job") != -1:
                result.remove(i)

        return len(result), result


# nltk.downloader.download('vader_lexicon')
sentiment_analyzer = SentimentIntensityAnalyzer()


def polarity_scores(doc):
    return sentiment_analyzer.polarity_scores(doc.text)


Doc.set_extension('polarity_scores', getter=polarity_scores)


def determine_y_n(nlp, text):
    if text == "y" or text == "Y":
        return 1
    if text == "n" or text == "N":
        return -1

    doc = nlp(text.encode('utf8').decode('utf8'))
    dict = doc._.polarity_scores
    if dict.get('compound') > 0:
        return 1
    elif dict.get('compound') < 0:
        return -1
    else:
        return 0


def determine_emotion(nlp, text):
    doc = nlp(text.encode('utf8').decode('utf8'))
    dict = doc._.polarity_scores
    return dict.get('compound')


def determine_modify(num):
    num = int(num)
    if num == 4 or num == 6:
        return "address"
    elif num == 9:
        return "calendar"
    else:
        return ""


def employ_modify(num):
    num = int(num)
    if num == 4 or num == 5:
        return "address"
    elif num == 7:
        return "asset"
    elif num == 8:
        return "full_part"
    elif num == 11 or num == 12:
        return "calendar"
    elif num == 13:
        return "remote_specific"
    elif num == 14:
        return "probationary"
    # elif num==14:
    # 	return "probationary"
    else:
        return ""





