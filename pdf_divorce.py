import user
import datetime
from fpdf import FPDF
import database
import datetime


def generate_pdf_divorce(answer, userid, num_temp):
    t = datetime.datetime.now()
    date = t.strftime("%Y-%m-%d")

    m = ["Miss ", "Mr. "]

    if answer[9] == '0':
        x = 0
    else:
        x = 1

    age = []
    adopt = []
    no_adopt = []
    child_m = []
    if answer[23].find("y") != -1:
        if (answer[24].lower()).find("mother") != -1:
            spousal_m = m[0] + answer[0]
            no_spousal = m[1] + answer[1]
        else:
            no_spousal = m[0] + answer[0]
            spousal_m = m[1] + answer[1]

    if x == 1:
        num = int(answer[9])

        children = answer[10]
        born = answer[11]
        university = answer[12]
        main = answer[13]
        who_main = answer[14]
        amount_main = answer[15]
        modify_main = answer[16]

        for i in who_main:
            if (i.lower()).find("mother") != -1:
                child_m.append(m[0] + answer[0])
            if (i.lower()).find("father") != -1:
                child_m.append(m[1] + answer[1])
            else:
                child_m.append("0")

        for i in range(num):
            now = datetime.datetime.now()
            born_date = datetime.datetime.strptime(born[i], "%Y-%m-%d")
            delta = now - born_date
            agei = delta.days / 365
            age.append(agei)

        for i in range(len(answer[18])):
            if (answer[18][i].lower()).find("mother") != -1:
                adopt.append(m[0] + answer[0])
                no_adopt.append(m[1] + answer[1])
            elif (answer[18][i].lower()).find("father") != -1:
                adopt.append(m[1] + answer[1])
                no_adopt.append(m[0] + answer[0])
            else:
                adopt.append("0")
                no_adopt.append("0")
    else:
        num = 0

    asset_m = answer[27]
    asset_f = answer[28]

    # answer = ['Mary', 'Peter','123456','hkust','654321','kowloon','45','50','10th May 2010','Tom']

    pdf = FPDF()

    # page 1
    pdf.add_page()
    pdf.set_font('Times', 'B', 15)
    pdf.cell(100, 50, "Mediated Settlement Agreement")
    pdf.ln(100)
    pdf.set_font('Times', 'B', 30)
    pdf.cell(100, 50, "Mediated Settlement Agreement")
    pdf.ln(10)
    pdf.cell(100, 50, "(Family Mediation)")

    pdf.ln(50)
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, ('Date: %s' % date))

    pdf.ln(20)
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, ('Miss  %s  Mother' % answer[0]))
    pdf.ln(15)
    pdf.cell(0, 5, 'and')
    pdf.ln(15)
    pdf.cell(0, 5, ('Mr.  %s  Father' % answer[1]))

    # page 2
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 15, ('THIS AGREEMENT IS MADE ON the %s :' % date), 1, 1, 'C')
    pdf.ln(10)
    pdf.cell(0, 5, 'BETWEEN')
    pdf.ln(10)
    pdf.cell(0, 5, ('1). Miss ' + answer[0] + ' Mother(hereinafter referred to as "Miss ' + answer[0] + '")'))
    pdf.ln()
    pdf.cell(0, 5, ('     HKID no: %s' % answer[2]))
    pdf.ln()
    pdf.cell(0, 5, ('     Address: %s' % answer[3]))
    pdf.ln(10)
    pdf.cell(0, 5, ('1). Mr. ' + answer[1] + ' Father(hereinafter referred to as "Mr. ' + answer[1] + '")'))
    pdf.ln()
    pdf.cell(0, 5, ('     HKID no: %s' % answer[4]))
    pdf.ln()
    pdf.cell(0, 5, ('     Address: %s' % answer[5]))
    pdf.ln(10)
    pdf.cell(0, 5, '(and collectively hereinafter the "Parties")')
    pdf.ln(20)

    # content begin
    # 1.foreword
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, '1.  Foreword')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5,
                   '1.1  This Agreement is a legally binding document. Before signing this Agreement, both Parties should read it carefully and make sure that they have clearly understood all the terms and contents contained herein. Before signing this Agreement, all Parties shall consider whether they should seek independent legal, financial and/or other professional advice(s).')
    pdf.ln(15)

    # 2.preamble
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, '2.  Preamble')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5, (
                '2.1  In relation to the joint application for the Family Mediation (the "Case") filed by the Parties to the Hong Kong Mediation and Arbitration Centre dated ' + date + ', Miss ' +
                answer[0] + ' and Mr. ' + answer[
                    1] + ' attended the mediation (the "Mediation") with Mr. Albert So (the "Family Mediator") in May 2018 in relation to a number of issues arising from their separation of marriage.'))
    pdf.ln(7)
    pdf.multi_cell(0, 5,
                   '2.2  Upon the completion of the said Mediation, both Parties agreed to settle the Case in accordance with all the terms and conditions contained herein.')
    pdf.ln(15)

    # 3.mediated settlement terms
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, '3.  Mediated Settlement Terms')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5, '3.1  This Agreement is predicated on the following facts:')
    pdf.ln(7)
    pdf.multi_cell(0, 5, ('      i.  Mr. ' + answer[1] + ' is aged ' + answer[
        7] + ' at the time of execution of this Agreement;'))
    pdf.ln(7)
    pdf.multi_cell(0, 5, ('      ii.  Miss ' + answer[0] + ' is aged ' + answer[
        6] + ' at the time of execution of this Agreement;'))
    pdf.ln(7)
    pdf.multi_cell(0, 5, ('      iii.  The Parties were legally married on ' + answer[8] + ';'))
    pdf.ln(7)
    pdf.multi_cell(0, 5, ('      iv.  Due to irretrievable breakdown of marriage, the Parties separated on ' + date))

    # add more here
    if x == 1:
        pdf.ln(7)
        pdf.multi_cell(0, 5, ('      v.  The parties have ' + answer[9] + ' children, namely,:'))
        i = 0
        for i in range(num):
            pdf.multi_cell(0, 5,
                           ('          (' + str(i + 1) + ') ' + children[i] + ' who was born on ' + born[i] + ';'))
        pdf.ln(7)
        pdf.multi_cell(0, 5, ('      vi. The children will live like the following since the date of seperation:'))
        i = 0
        for i in range(num):
            if age[i] >= 18:
                pdf.multi_cell(0, 5, ('          (' + str(i + 1) + ') ' + children[
                    i] + ' has already grown up (above 18 years old);'))
            else:
                pdf.multi_cell(0, 5,
                               ('          (' + str(i + 1) + ') ' + children[i] + ' will live with ' + adopt[i] + ';'))

    pdf.ln(15)

    # 4.CARING ARRANGEMENTS FOR THE CHILDREN
    if x == 1:
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0, 5, '4.  Caring Arrangements for the children')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        pdf.cell(0, 5, 'The Parties hereby agreed that:')
        pdf.ln(7)
        i = 0
        while i < num:
            if age[i] < 18:
                pdf.multi_cell(0, 5, '4.' + str(i + 1) + adopt[i] + ' shall keep ' + no_adopt[
                    i] + ' informed of the caring arrangements for ' + children[i] + ';')
                pdf.ln(7)
            i = i + 1

        pdf.multi_cell(0, 5, '4.' + str(
            i + 1) + '  Both Parties shall ensure that they will communicate to each other, or through a third party mediator, any change(s) in their personal relationships with respect of the Children\'s well-being;')
        pdf.ln(7)
        i = i + 1
        pdf.multi_cell(0, 5, '4.' + str(i + 1) + '  Miss. ' + answer[0] + ' and Mr. ' + answer[
            1] + ' shall take care of, and exercise her best endeavor to be aware of, the Children\'s emotional well-being at all times.')
        pdf.ln(15)

        # 5.	PARENTING PLAN
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0, 5, '5.  Parenting plan')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        pdf.multi_cell(0, 5,
                       '5.1  Both Parties acknowledge that they have had difficulty when communicating with each other due to the past problems in the course of marriage. That being the case, both Parties agree that they shall move on and agree that they shall mediate to ensure that the Children\'s well-being will be taken into account at all the times and particularly in respect of the family transition.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '5.2  Both parties agree to provide information on the Children\'s well-being to each other from time to time.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '5.3  Subject to Children\'s consent, Both parties will encourage the Children to forward their photos to the other one.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '5.4  Both parites agrees to continue to encourage Children to attend and receive education at school, at home, and will continue to provide them opportunities for learning through extra curricula activities')
        pdf.ln(7)
        pdf.multi_cell(0, 5, '5.5  The Parties agree that they will exercise their best endeavor to:')
        pdf.ln(7)
        pdf.multi_cell(0, 5, (
            '      i.  resolve their conflicts, if any, effectively by listening to each other\'s concerns;'))
        pdf.ln(7)
        pdf.multi_cell(0, 5, (
            '      ii.  agree that neither of them will attack each other verbally and will be careful in their use of language towards each other;'))
        pdf.ln(7)
        pdf.multi_cell(0, 5, ('      iii.  respect and take into account the views of the other;'))
        pdf.ln(7)
        pdf.multi_cell(0, 5, (
            '      iv.  choose to take a "time out" should discussions become heated, rather than withdraw, and to re-engage communication when appropriate;'))
        pdf.ln(7)
        pdf.multi_cell(0, 5, (
            '      v.  not to argue in front of the Children and to ensure that there will be no adult confrontation in front of the Children;'))
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       ('      vi.  use a third party mediator if either Party cannot agree on any discussion points.'))
        pdf.ln(7)
        pdf.multi_cell(0, 5, '5.6  In respect of the Children, both Parties agree to exercise their best endeavor to:')
        pdf.ln(7)
        pdf.multi_cell(0, 5, ('      i.  teach the Children to respect for themselves and for others;'))
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       ('      ii.  support Children in their own decision in relation to their Chinese heritage;'))
        pdf.ln(7)
        pdf.multi_cell(0, 5, (
            '      iii.  make the best health decisions for the Children by ensuring that the Children receives a balanced nutritional diet and to actively promote good eating habits and emphasize the importance of sport and exercise;'))
        pdf.ln(7)
        pdf.multi_cell(0, 5, ('      iv.  use counseling services when necessary and appropriate.'))
        pdf.ln(15)

        # 6. 	CUSTODY
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0, 5, '6.  Custody')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        i = 0
        j = 1
        while i < num:
            if age[i] < 18:
                if answer[18][i].find("sole") != -1:
                    pdf.multi_cell(0, 5, '6.' + str(j) + '  The Parties agree that ' + adopt[
                        i] + ' shall have sole custody of ' + children[i] + ' until ' + children[
                                       i] + ' has reached 18 years of age.')
                else:
                    pdf.multi_cell(0, 5, '6.' + str(j) + '  The Parties agree that ' + adopt[
                        i] + ' shall have joint custody (major charge) of ' + children[i] + ' until ' + children[
                                       i] + ' has reached 18 years of age.')
                j = j + 1
                pdf.ln(7)
            i = i + 1

        pdf.multi_cell(0, 5, '6.' + str(
            j) + '  The Parties agree that the one who has major charge of custody of children shall provide all education, health and welfare authorities or any written authorization which will allow the other one to get access to reports and information pertaining to the Children\'s education, health and welfare in addition to the agreement indicated herein above.')
        j = j + 1
        pdf.ln(7)
        pdf.multi_cell(0, 5, '6.' + str(
            j) + '  The Parties agree that they will keep each other updated with their respective email addresses, telephone numbers, residential address and will advise each other of any change(s) within 1 months to these details.')
        pdf.ln(15)

        # 7. 	CARE AND CONTROL
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0, 5, '7.  Care and Control')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        for i in range(num):
            if age[i] < 18:
                pdf.multi_cell(0, 5,
                               'The Parties agree that ' + adopt[i] + ' shall have the sole care and control of ' +
                               children[i] + '.')
                pdf.ln(7)
        pdf.ln(15)

        # 8. 	ACCESS
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0, 5, '8.  Access')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        pdf.multi_cell(0, 5,
                       '8.1  Both Parties acknowledge that it is the Children\'s right to maintain contact and relationship with both Parties.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '8.2  The Parties agree that they can have contact with the Children by telephone and/or other electronic telecommunications at reasonable times.')
        pdf.ln(7)
        pdf.multi_cell(0, 5, '8.3  The Parties agree the following short term access arrangements:')
        pdf.ln(7)
        for i in range(num):
            if age[i] < 18:
                pdf.multi_cell(0, 5, '    For ' + children[i] + ':')
                pdf.ln(7)
                access = answer[22][i].split(";")
                j = 1

                for n in range(len(access)):
                    pdf.multi_cell(0, 5, ('      (' + str(j) + ') ' + access[n]) + ';')
                    pdf.ln(7)
                    j = j + 1

        pdf.ln(15)

        # 9. 	CHILDREN AND SPOUSAL MAINTENANCE
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0, 5, '9.  Children and Spousal Maintenance')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        # modify later here!!!
        if answer[23].find("y") != -1:
            if answer[25].find("once") != -1:
                pdf.multi_cell(0, 5, (
                            '9.1  ' + spousal_m + ' shall pay the lump sum spousal maintenance ("Spousal Maintenance") in the sum of HKD' +
                            answer[
                                26] + ' together to ' + no_spousal + '. Such Spousal Maintenance is guaranteed to be paid by ' + spousal_m + ' to ' + no_spousal + ' as a lump sum payment.'))
            else:
                pdf.multi_cell(0, 5, (
                            '9.1  ' + spousal_m + ' shall pay the monthly spousal maintenance ("Spousal Maintenance") in the sum of HKD' +
                            answer[
                                26] + ' per month to ' + no_spousal + ' [on or before the fifth calendar date of each month], with payment instructions to be specified by ' + no_spousal + ' from time to time. Such Spousal Maintenance is guaranteed to be paid by ' + spousal_m + ' to ' + no_spousal + ' until ' + no_spousal + ' get married again or one of the parties dead.'))

            pdf.ln(7)
        j = 2
        for i in range(num):
            if main[i].find('y') != -1:
                pdf.multi_cell(0, 5, ('9.' + str(j) + '  ' + child_m[
                    i] + ' shall be responsible for all the school fees, health insurance and reasonable living allowances (monthly payment about ' +
                                      amount_main[i] + ' HKD) for ' + children[
                                          i] + ' ("Children Maintenance") until he/she 18 years old or finish full-time study. Any major expense(s) for the Children Maintenance must be agreed by ' +
                                      child_m[i] + ' before it is incurred. '))
                pdf.ln(7)
                j = j + 1
        pdf.multi_cell(0, 5, (
            'Save for the aforementioned, the Parties agree that neither of them shall have the legal right to make any further claim(s) against the other regarding Children and/or spousal maintenance.'))
        pdf.ln(15)
    if x == 0:
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0, 5, '4.  Children and Spousal Maintenance')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        # modify later here!!!
        if answer[23].find("y") != -1:
            if answer[25].find("once") != -1:
                pdf.multi_cell(0, 5, (
                            '' + spousal_m + ' shall pay the lump sum spousal maintenance ("Spousal Maintenance") in the sum of HKD' +
                            answer[
                                26] + ' together to ' + no_spousal + '. Such Spousal Maintenance is guaranteed to be paid by ' + spousal_m + ' to ' + no_spousal + ' as a lump sum payment.'))
            else:
                pdf.multi_cell(0, 5, (
                            '' + spousal_m + ' shall pay the monthly spousal maintenance ("Spousal Maintenance") in the sum of HKD' +
                            answer[
                                26] + ' per month to ' + no_spousal + ' [on or before the fifth calendar date of each month], with payment instructions to be specified by ' + no_spousal + ' from time to time. Such Spousal Maintenance is guaranteed to be paid by ' + spousal_m + ' to ' + no_spousal + ' until ' + no_spousal + ' get married again or one of the parties dead.'))
            pdf.ln(7)
        pdf.multi_cell(0, 5, (
            'Save for the aforementioned, the Parties agree that neither of them shall have the legal right to make any further claim(s) against the other regarding spousal maintenance.'))
        pdf.ln(15)

    # 10. 	ASSET DIVISION
    pdf.set_font('Times', 'B', 14)
    if x == 1:
        pdf.cell(0, 5, '10.  Asset Division')
    elif x == 0:
        pdf.cell(0, 5, '5.  Asset Division')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5, 'The Parties agree that the matrimonial assets shall be distributed as follow:')
    pdf.ln(7)
    pdf.multi_cell(0, 5, 'To and for the benefit of Miss. ' + answer[0] + ':')
    pdf.ln(7)

    # add here later
    i = 0
    while i < len(asset_m):
        pdf.multi_cell(0, 5, ('    ' + str(i + 1) + '.  ' + asset_m[i]))
        i = i + 1
        pdf.ln(7)
    pdf.multi_cell(0, 5, 'The remaining matrimonial assets shall go to Mr. ' + answer[1] + ', including:')
    pdf.ln(7)
    # add here later
    i = 0
    while i < len(asset_f):
        pdf.multi_cell(0, 5, ('    ' + str(i + 1) + '.  ' + asset_f[i]))
        i = i + 1
        pdf.ln(7)

    # 11.	MISCELLANEOUS
    pdf.set_font('Times', 'B', 14)
    if x == 1:
        pdf.cell(0, 5, '11.  Miscellaneous')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        pdf.multi_cell(0, 5,
                       '11.1  The Parties acknowledge that they have considered to seek independent legal and/or other professional advice(s) on all matters contained in this Agreement')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '11.2  The Parties further agree to attempt to resolve any dispute arising out of, or in connection with, this Agreement prior to initiating any legal proceedings.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '11.3  This Agreement is made by the Parties and they agree that all the terms contained herein be formalized as a Consent Order to be approved by the Family Court of HKSAR.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '11.4  Save for those exceptions as permitted by the laws of HKSAR, the Parties agreed to keep confidential all the settlement terms as contained herein. Unless prior written consent has been obtained from both Parties, no Party shall disclose any content(s) of this Agreement to any third party.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '11.5  The Parties hereby confirmed that they are signing this Agreement voluntarily and upon sufficient consideration. The Parties also confirmed that they have not relied on any opinion, either professional or personal, provided by the mediator for the purpose of reaching this Agreement.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '11.6  This Agreement shall be executed and interpreted in accordance with the laws of HKSAR.')
        pdf.ln(30)
    elif x == 0:
        pdf.cell(0, 5, '6.  Miscellaneous')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        pdf.multi_cell(0, 5,
                       '6.1  The Parties acknowledge that they have considered to seek independent legal and/or other professional advice(s) on all matters contained in this Agreement')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '6.2  The Parties further agree to attempt to resolve any dispute arising out of, or in connection with, this Agreement prior to initiating any legal proceedings.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '6.3  This Agreement is made by the Parties and they agree that all the terms contained herein be formalized as a Consent Order to be approved by the Family Court of HKSAR.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '6.4  Save for those exceptions as permitted by the laws of HKSAR, the Parties agreed to keep confidential all the settlement terms as contained herein. Unless prior written consent has been obtained from both Parties, no Party shall disclose any content(s) of this Agreement to any third party.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '6.5  The Parties hereby confirmed that they are signing this Agreement voluntarily and upon sufficient consideration. The Parties also confirmed that they have not relied on any opinion, either professional or personal, provided by the mediator for the purpose of reaching this Agreement.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '6.6  This Agreement shall be executed and interpreted in accordance with the laws of HKSAR.')
        pdf.ln(30)

    # end
    pdf.cell(0, 15, '*****', 1, 1, 'C')

    # signature page
    pdf.add_page()
    pdf.set_font('Times', 'B', 16)
    pdf.cell(0, 15, 'Signature Page', 1, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5,
                   'The Parties hereby sign this Agreement on the date as stated at the beginning of this Agreement.')
    pdf.ln(70)
    pdf.set_font('Times', 'B', 12)
    pdf.multi_cell(0, 5,
                   '_____________________                                                            _____________________')
    pdf.multi_cell(0, 5, 'Signature of ' + answer[
        0] + '                                                                      Signature of ' + answer[1])
    pdf.multi_cell(0, 5, 'HKID no:' + answer[
        2] + '                                                                        HKID no:' + answer[4])

    # back page
    pdf.add_page()
    pdf.ln(10)
    pdf.set_font('Times', 'U', 12)
    pdf.cell(0, 5, 'Data: ' + date)
    pdf.ln(50)
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, answer[0] + ' Mother', 0, 0, 'C')
    pdf.ln(10)
    pdf.cell(0, 5, 'and', 0, 0, 'C')
    pdf.ln(10)
    pdf.cell(0, 5, answer[1] + ' Father', 0, 0, 'C')
    pdf.ln(50)
    pdf.cell(0, 5, '-------------------------------------------------', 0, 0, 'C')
    pdf.ln(15)
    pdf.cell(0, 5, 'Mediated Settlement Agreement', 0, 0, 'C')
    pdf.ln(15)
    pdf.cell(0, 5, '-------------------------------------------------', 0, 0, 'C')

    filename = "./static/divorce_pdf/divorce_" + str(userid) + "_" + str(num_temp) + ".pdf"
    pdf.output(filename, 'F')
