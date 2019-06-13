import user
import datetime
from fpdf import FPDF
import database


def generate_pdf_employment(answer, userid, num_temp):
    t = datetime.datetime.now()
    date = t.strftime("%Y-%m-%d")

    pdf = FPDF()

    remote = answer[13]
    probationary = answer[15]
    health = answer[18]
    commission = answer[19]

    if answer[7].find("full") != -1:
        full = 1
    else:
        full = 0

    pdf.add_page()
    pdf.set_font('Times', 'B', 15)
    pdf.cell(0, 5, 'PRIVATE & CONFIDENTIAL')
    pdf.ln(8)
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, answer[2], 0, 0, 'R')
    pdf.ln(8)
    pdf.cell(0, 5, answer[3], 0, 0, 'R')
    pdf.ln(10)
    pdf.cell(0, 5, date)
    pdf.ln(10)
    pdf.cell(0, 5, answer[1])
    pdf.ln(5)
    pdf.cell(0, 5, answer[4])
    pdf.ln(10)
    pdf.cell(0, 5, 'Dear ' + answer[0] + ',')
    pdf.ln(10)

    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, 'LETTER OF EMPLOYMENT', 0, 0, 'C')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    if full == 1:
        pdf.multi_cell(0, 5, 'On behalf of ' + answer[
            2] + ' (the "Employer"), I am delighted to offer you employment on a full-time basis in the role of ' +
                       answer[5] + '. It is intended for you to commence your employment on ' + answer[11] + '.')
    else:
        pdf.multi_cell(0, 5, 'On behalf of ' + answer[
            2] + ' (the "Employer"), I am delighted to offer you employment on a part-time basis in the role of ' +
                       answer[5] + '. It is intended for you to commence your employment on ' + answer[11] + '.')
    pdf.ln(10)
    pdf.multi_cell(0, 5,
                   'Please read through this letter carefully and indicate your acceptance of the offer by signing and returning a copy of this letter on or before ' +
                   answer[12] + '.')
    pdf.ln(15)

    # 1. position
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, '1.  Your Position')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5, '1.1  Your will be employed in the role of ' + answer[5] + '.')
    pdf.ln(7)
    pdf.multi_cell(0, 5,
                   '1.1  In addition to any duties allocated by the Employer from time to time, your position will involve the duties set out below:')
    pdf.ln(7)
    x = answer[6].split(";")
    for i in range(len(x) - 1):
        pdf.multi_cell(0, 5, x[i] + ';', 0, 0, 'C')
    pdf.multi_cell(0, 5, x[len(x) - 1] + '.', 0, 0, 'C')
    pdf.ln(15)

    # 2. location
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, '2.  Location')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    if remote == 1:
        pdf.multi_cell(0, 5,
                       'You will be based at the address shown below, although we may direct you to work at different locations from time to time:')
        pdf.ln(7)
        pdf.multi_cell(0, 5, answer[14], 0, 0, 'C')
    else:
        pdf.multi_cell(0, 5,
                       'Your duties may be performed from such location as you see fit, although we may direct you to work from specific locations.')

    pdf.ln(15)

    # probationary period--not mandatory
    n = 3
    if probationary == 1:
        n = 4
        pdf.set_font('Times', 'B', 14)
        pdf.cell(0, 5, '3.  Probationary Period')
        pdf.ln(10)
        pdf.set_font('Times', '', 12)
        pdf.multi_cell(0, 5,
                       '3.1  Your employment is subject to the satisfactory completion of a probationary period of ' +
                       answer[16] + ' weeks.')
        pdf.ln(7)
        pdf.multi_cell(0, 5,
                       '3.2  The probationary period is designed to grant the Employer time to assess whether you are able to fulfill your role with the Employer. During the probationary period your employment may be terminated by either you or the Employer upon providing one (1) week written notice (or payment in lieu of that notice).')
        pdf.ln(15)

    # 3. hours of work
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, str(n) + '.  Hours of work')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    if full == 1:
        pdf.multi_cell(0, 5, str(
            n) + '.1  As a full-time employee you will be required to devote substantially the whole of your time and attention during the Employer\'s ordinary business hours to the performance of your duties under this agreement.')
    else:
        pdf.multi_cell(0, 5, str(
            n) + '.1  As a part-time employee, the total number of hours you will be expected to work per week is ' +
                       answer[8] + '.')
    pdf.ln(7)
    pdf.multi_cell(0, 5, str(
        n) + '.2  You will not be entitled to receive any remuneration for work performed outside of the hours referred to in sub-clause 3.1 above.')
    pdf.ln(15)

    # 4. Salary and benefits
    n = n + 1
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, str(n) + '.  Salary and Benefits')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5, str(n) + '.1  Your monthly salary will be HKD ' + answer[9] + '.')
    pdf.ln(7)
    pdf.multi_cell(0, 5, str(n) + '.2  This salary will be paid by monthly deposit into your nominated account.')
    pdf.ln(7)
    m = 3
    if commission == 1:
        pdf.multi_cell(0, 5, str(n) + '.' + str(
            m) + '  In addition to your salary, you will be entitled to receive commission on such basis as set out in your employment contract or the commission policy of the Employer.')
        pdf.ln(7)
        m = m + 1
    if health == 1:
        pdf.multi_cell(0, 5, str(n) + '.' + str(
            m) + '  You will be entitled to join the medical insurance scheme maintained by the Employer during your employment. Your entitlements will be subject to such terms and rules which the Employer may establish or vary from time to time.')
        pdf.ln(7)
        m = m + 1
    pdf.multi_cell(0, 5, str(n) + '.' + str(
        m) + '  Deductions will be made from your salary to make applicable amount of mandatory contributions to the Mandatory Provident Fund or other funds in accordance with the provisions of applicable laws.')
    pdf.ln(15)

    # 5. leave
    n = n + 1
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, str(n) + '.  Leave')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5, str(n) + '.1  You will be entitled to paid annual leave of ' + answer[
        10] + ' working days each year.')
    pdf.ln(7)
    pdf.multi_cell(0, 5, str(
        n) + '.2  You may also be entitled to sick leave and parental leave in accordance with the Employer\'s policies and applicable legislations and regulations.')
    pdf.ln(15)

    # 6. Company policies
    n = n + 1
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, str(n) + '.  Company policies')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5,
                   'You agree that the Employer\'s policies, as amended or replaced from time to time, shall be binding upon you but shall not form part of the employment contract.')
    pdf.ln(15)

    # 7. Confidentiality and intellectual property
    n = n + 1
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, str(n) + '.  Confidentiality and intellectual property')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5, str(
        n) + '.1  You agree that you will not divulge any of the confidential information or trade secrets of the Employer to any person, whether during or after the termination of your employment.')
    pdf.ln(7)
    pdf.multi_cell(0, 5, str(
        n) + '.2  You agree that you will not use, attempt to use, or assist another person in using any confidential information you may acquire in the course of your employment in a manner which may cause loss to the Employer.')
    pdf.ln(15)

    # 8. Termination
    n = n + 1
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, str(n) + '.  Termination')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5, str(n) + '.1  Either party may terminate your employment contract by providing ' + answer[
        17] + ' weeks of written notice (or payment in lieu of notice) to the other party.')
    pdf.ln(7)
    pdf.multi_cell(0, 5, str(
        n) + '.2  Notwithstanding sub-clause 8.1 above, the Employer may terminate this agreement by notice effective immediately without payment (except salary accrued to the date of termination) where you have committed an act of wilful or serious misconduct, are significantly neglectful of your duties, or you are in serious breach of your Contract of Employment.')
    pdf.ln(15)

    # 9. Conditions of employment
    n = n + 1
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 5, str(n) + '.  Conditions of employment')
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5,
                   'This Letter of Offer contains the proposed terms and conditions of your employment with the Employer and is subject to:')
    pdf.ln(7)
    pdf.multi_cell(0, 5, '(a).  documentary evidence of your right to work in Hong Kong;')
    pdf.ln(7)
    pdf.multi_cell(0, 5, '(b).  satisfactory references, including your current and most recent employer;')
    pdf.ln(7)
    pdf.multi_cell(0, 5, '(c).  preparation and execution of a formal contract of employment.')
    pdf.ln(7)

    # signature
    pdf.multi_cell(0, 5, '*I, ' + answer[
        0] + ', accept and agree to the proposed terms of employment and request that the Employer prepare a formal contract of employment for execution.')

    print("employment letter number!: " + str(num_temp))
    filename = "./static/employment_pdf/employment_" + str(userid) + "_" + str(num_temp) + ".pdf"
    # filename = "Test_employment.pdf"
    pdf.output(filename, 'F')











