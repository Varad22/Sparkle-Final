from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import Flask
from flask_mail import Mail
import speech_recognition as sr
import gspread
import pandas as pd
import numpy as np
import pandas as pd
import PyPDF2
from fpdf import FPDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
import pandas as pd
import numpy as np
import pickle
from collections import Counter
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import math
from face_detector import get_face_detector, find_faces
from face_landmarks import get_landmark_model, detect_marks
import time
import spacy
global Total_time
Total_time = 0
nlp = spacy.load("en_core_web_lg")


app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sparkle'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'as1303879@gmail.com'
app.config['MAIL_PASSWORD'] = 'lincolnab'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

mysql = MySQL(app)
r = sr.Recognizer()  

cal_model1=pickle.load(open('dyscal1.pkl','rb'))
cal_model2=pickle.load(open('dyscal2.pkl','rb'))
cal_model3=pickle.load(open('dyscal3.pkl','rb'))
cal_model4=pickle.load(open('dyscal4.pkl','rb'))
cal_model5=pickle.load(open('dyscal_model.pkl','rb'))


lex_model1=pickle.load(open('dyslex1.pkl','rb'))
lex_model2=pickle.load(open('dyslex2.pkl','rb'))
lex_model3=pickle.load(open('dyslex_model.pkl','rb'))   



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/student_login', methods=['GET', 'POST'])
def student_login():

    if request.method == 'POST':
        print("gg")
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        print(email)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM p_creds WHERE p_email = %s AND password = %s ', [email, password])
        # Fetch one record and return result

        account = cursor.fetchone()
        session['p_email'] = account['p_email']
        # If account exists in accounts table in out database
        if account:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM feedback_dyslexia WHERE p_email = %s ', [session['p_email']])
            solution = cursor.fetchone()
            cursor.execute('SELECT * FROM feedback_dyscalculia WHERE p_email = %s ', [session['p_email']])
            solution2 = cursor.fetchone()
            cursor.execute('SELECT * FROM feedback_dysgraphia WHERE p_email = %s ', [session['p_email']])
            solution3 = cursor.fetchone()
            cursor.execute('SELECT * FROM feedback_adhd WHERE p_email = %s ', [session['p_email']])
            solution4 = cursor.fetchone()
            # cursor.execute('SELECT * FROM lex_test1 WHERE p_email = %s ', [email])
            # solution3 = cursor.fetchone()
            if solution and solution and solution2 and solution3 and solution4:
                session['loggedin'] = True
                session['p_email'] = account['p_email']
                session['school'] = account['school']
                session['s_name'] = account['s_name']
            # account exists and test taken, so redirect to profile page
                return redirect(url_for('student_profile'))
            else:
                session['loggedin'] = True
                session['p_email'] = account['p_email']
                session['school'] = account['school']
                session['s_name'] = account['s_name']
                return redirect(url_for('sections'))
            # account exists and test NOT taken, so redirect to exam page page

    return render_template('signin.html')

@app.route('/sections', methods = ['GET', 'POST'])
def sections():
    name = session['s_name']
    sections_dict = {'Section 1':["../static/assets/img/test-section/section-i.jpg","/instructions1"],'Section 2':["../static/assets/img/test-section/section-ii.jpg","/instructions2"],'Section 3':["../static/assets/img/test-section/section-iii.jpg","/instructions3"],'Section 4':["../static/assets/img/test-section/section-iv.jpg","/instructions4"]}
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM feedback_dyslexia WHERE p_email = %s ', [session['p_email']])
    solution = cursor.fetchone()
    cursor.execute('SELECT * FROM feedback_dyscalculia WHERE p_email = %s ', [session['p_email']])
    solution2 = cursor.fetchone()
    cursor.execute('SELECT * FROM feedback_dysgraphia WHERE p_email = %s ', [session['p_email']])
    solution3 = cursor.fetchone()
    cursor.execute('SELECT * FROM feedback_adhd WHERE p_email = %s ', [session['p_email']])
    solution4 = cursor.fetchone()

    if solution:
        del sections_dict['Section 1']
    if solution2:
        del sections_dict['Section 2']
    if solution3:
        del sections_dict['Section 3']
    if solution4:
        del sections_dict['Section 4']
    if solution and solution2 and solution3 and solution4:
        return redirect(url_for('student_profile'))
    return render_template('sections.html',sections_dict=sections_dict, name=name)




@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    s_id = 00000
    if request.method == 'POST':
        s_name = request.form['s_name']
        age = request.form['age']
        password = request.form['password']
        p_name = request.form['p_name']
        school = request.form['school']
        p_email = request.form['p_email']
        p_phone = request.form['p_phone']

        print(s_name, age, password, p_name, school, p_email, p_phone)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO p_creds(s_name, age, p_name, school, p_email, p_phone, password) VALUES(%s,%s,%s,%s,%s,%s,%s)', [
                       s_name, age, p_name, school, p_email, p_phone, password])
        mysql.connection.commit()
        # sendmail(s_name, password, p_name, school, p_email, p_phone)

        msg = 'Successfully registered! Please Sign-In'
        print('done')
        # student will be redirected for a test immediately
        return redirect(url_for('student_login'))

    return render_template('signup.html')


@app.route('/d_signup', methods=['GET', 'POST'])
def d_signup():
    if request.method == 'POST':
        d_name = request.form['d_name']
        d_password = request.form['d_password']
        d_email = request.form['mail']
        desi = request.form['Designation']
        d_no = request.form['num']
        d_school = request.form['d_school']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO d_creds VALUES(%s,%s,%s,%s,%s,%s)', [d_name,desi,d_email,d_no,d_password,d_school])
        mysql.connection.commit()
        return redirect(url_for('d_login'))
    return render_template('d_signup.html')


@app.route('/d_login', methods=['GET', 'POST'])
def d_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM d_creds WHERE d_pass = %s ', [password])
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['d_mail'] = account['d_mail']
            session['d_school'] = account['d_school']
            return redirect(url_for('dr_profile'))

    return render_template('d_login.html')


@app.route('/dr_landing')
def dr_landing():
    return render_template('dr_landing.html')


@app.route('/doctor-patient-profile')
def dpp():
    return render_template('doctor-patient-profile.html')


@app.route('/doctor-profile')
def dr_profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT d_name,designation,d_mail,d_phone,d_school FROM d_creds WHERE d_mail = %s ', [session['d_mail']])
    account = cursor.fetchone()
    
    return render_template('doctor-profile.html',account=account)


@app.route('/student_profile')
def student_profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT s_name,age,school FROM p_creds WHERE p_email = %s ', [session['p_email']])
    account = cursor.fetchone()
    return render_template('student_profile.html',name=account['s_name'],age=account['age'],school=account['school'])


@app.route('/student_profile1', methods=['GET', 'POST'])
def student_profile1():
    test = ''
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('18sXYVa_hqEAcZAuuzXplbqKcKsLj0dPZ80V5ZuNw9uI')
    Worksheet = sh.worksheet('Sheet1')
    list_of_lists = Worksheet.get_all_values()
    questions_list = []
    responses_of_parent = []

    # student_name = 'Ronit Bhamere'
    # q1 = list_of_lists[0][1]
    # q2 = list_of_lists[0][2]
    # q3 = list_of_lists[0][3]
    # q4 = list_of_lists[0][4]
    # q5 = list_of_lists[0][5]
    # q6 = list_of_lists[0][6]
    # q7 = list_of_lists[0][7]
    # q8 = list_of_lists[0][8]
    # q9 = list_of_lists[0][9]
    # q10 = list_of_lists[0][10]
    # q11 = list_of_lists[0][11]
    # q12 = list_of_lists[0][12]
    # q13 = list_of_lists[0][13]
    # q14 = list_of_lists[0][14]
    # q15 = list_of_lists[0][15]
    # dic = {}

    # questions_list = [q1, q2, q3, q4, q5, q6,
    #                   q7, q8, q9, q10, q11, q12, q13, q14, q15]

    # for x in list_of_lists:
    #     if student_name in x[16]:
    #         a1 = x[1]
    #         a2 = x[2]
    #         a3 = x[3]
    #         a4 = x[4]
    #         a5 = x[5]
    #         a6 = x[6]
    #         a7 = x[7]
    #         a8 = x[8]
    #         a9 = x[9]
    #         a10 = x[10]
    #         a11 = x[11]
    #         a12 = x[12]
    #         a13 = x[13]
    #         a14 = x[14]
    #         a15 = x[15]
    #         student_id = x[18]

    # responses_of_parent = [a1, a2, a3, a4, a5, a6,
    #                        a7, a8, a9, a10, a11, a12, a13, a14, a15]
    # dic = dict(zip(questions_list, responses_of_parent))

    # print(dic)

    # # st_name = 'Ronit'

    # # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # # cursor.execute('SELECT * FROM analysis WHERE st_name=%s', [st_name])
    # # ana = cursor.fetchall()

    # # print(ana)

    # if request.method == 'POST' and 't1' in request.form:
    #     t1 = request.form.getlist('t1')
    #     t2 = request.form.getlist('t2')
    #     print(t1, t2)
    #     test = t1[0]

    # s_id = 123

    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('INSERT INTO courses VALUES(%s,%s)', [s_id, test])
    # mysql.connection.commit()



    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM sample')
    # lis = cursor.fetchall()

    # list1 = []
    # for i in range(len(lis)):
    #     x = lis[i]
    #     list_h = []
    #     for key in x.values():
    #         list_h.append(key)
    #     list1.append(list_h)
    # print(list1)

    # loaded_model = pickle.load(open('xg2.sav', 'rb'))

    # for i in list1:
    #     test = [i]
    #     print(test)
    #     output = return_top_n_pred_prob_df(3, loaded_model, test, "test")
    #     l = output.values.tolist()

    #     disease1 = l[0][1]
    #     disease2 = l[0][3]
    #     disease3 = l[0][5]
    #     acc1 = str(round(l[0][0]*100, 3))
    #     acc2 = str(round(l[0][2]*100, 3))
    #     acc3 = str(round(l[0][4]*100, 3))

    #     if disease1 == 1:
    #         disease1 = 'No Disease '
    #     elif disease1 == 2:
    #         disease1 = "Dyslexia "
    #     elif disease1 == 3:
    #         disease1 = "Dyscalculia "

    #     print(" The Probability of " + disease1 + " is : " + acc1)

    #     if disease2 == 1:
    #         disease2 = 'No Disease '
    #     elif disease2 == 2:
    #         disease2 = "Dyslexia "
    #     elif disease2 == 3:
    #         disease2 = "Dyscalculia "
    #     print(" The Probability of " + disease2 + " is : " + acc2)

    #     if disease3 == 1:
    #         disease3 = 'No Disease '
    #     elif disease3 == 2:
    #         disease3 = "Dyslexia "
    #     elif disease3 == 3:
    #         disease3 = "Dyscalculia "
    #     print(" The Probability of " + disease3 + " is : " + acc3)

    #     print(disease1, acc1, disease2, acc2, disease3, acc3)

    #     if disease1 == "No Disease is Identified":
    #         print("No treatment required.")
    #     elif (disease1 == "Dyslexia" or "Dyscalculia") and (disease2 == "Dyslexia" or "Dyscalculia"):
    #         print(disease1, acc1, disease2, acc2)


    # return render_template('student_profile1.html', dic=dic, disease1=disease1, acc1=acc1, disease2=disease2, acc2=acc2)


def return_top_n_pred_prob_df(n, model, X_test, column_name):
    predictions = model.predict_proba(X_test)
    preds_idx = np.argsort(-predictions)
    classes = pd.DataFrame(model.classes_, columns=['class_name'])
    classes.reset_index(inplace=True)
    top_n_preds = pd.DataFrame()
    for i in range(n):
        top_n_preds[column_name + '_prediction_{}_num'.format(
            i)] = [preds_idx[doc][i] for doc in range(len(X_test))]
        top_n_preds[column_name + '_prediction_{}_probability'.format(
            i)] = [predictions[doc][preds_idx[doc][i]] for doc in range(len(X_test))]
        top_n_preds = top_n_preds.merge(
            classes, how='left', left_on=column_name + '_prediction_{}_num'.format(i), right_on='index')
        top_n_preds = top_n_preds.rename(
            columns={'class_name': column_name + '_prediction_{}'.format(i)})
        try:
            top_n_preds.drop(
                columns=['index', column_name + '_prediction_{}_num'.format(i)], inplace=True)
        except:
            pass
    return top_n_preds





@app.route('/student_list')
def student_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM p_creds WHERE school=%s',[session['d_school']])
    email_list = cursor.fetchall() 
    
            

    return render_template('student_list.html',email_list=email_list)



#INSTRUCTION PAGES

@app.route('/instructions1')
def instructions():

    return render_template('instructions1.html')
    
@app.route('/instructions2')
def instructions2():

    return render_template('instructions2.html')
    
@app.route('/instructions3')
def instructions3():

    return render_template('instructions3.html')
    
@app.route('/instructions4')
def instructions4():

    return render_template('instructions4.html')


#FEEDBACK PAGES

@app.route('/feedback_dyslexia', methods = ['GET', 'POST'])
def feedback_dyslexia():
    name = session['s_name']
    if request.method == 'POST':
        ans1 = request.form['q1']
        ans2 = request.form['q2']
        ans3 = request.form['q3']
        ans4 = request.form.get('q4')
        print(ans1, ans2, ans3, ans4)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO feedback_dyslexia VALUES(%s,%s,%s,%s,%s)',
                    [session['p_email'], ans1, ans2, ans3, ans4])
        mysql.connection.commit()

        cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_word WHERE p_email=%s',[session['p_email']])
        word=cursor.fetchone()

        cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_sent WHERE p_email=%s',[session['p_email']])
        sent=cursor.fetchall()

        cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test1 WHERE p_email=%s',[session['p_email']])
        para=cursor.fetchone()

        cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test2 WHERE p_email=%s',[session['p_email']])
        para2=cursor.fetchone()

        cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_objects WHERE p_email=%s',[session['p_email']])
        obj=cursor.fetchone()

        cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_nonsensewords WHERE p_email=%s',[session['p_email']])
        nonwords=cursor.fetchone()

        cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_blendwords WHERE p_email=%s',[session['p_email']])
        blend=cursor.fetchone()


        lexacc = float(word['accuracy'])+float(sent[0]['accuracy'])+float(sent[1]['accuracy'])+float(para['accuracy'])+float(para2['accuracy'])+float(blend['accuracy'])+float(obj['accuracy'])+float(nonwords['accuracy'])
        lexacc = round(lexacc/8, 2)
        lexWa = 0
        lexWd = 0
        lexRPI = ''
        lexProficiency = ''
        lextask_management = ''


        if lexacc >= 0.75:
            lexWa = 490
            lexWd = 475
        elif lexacc >=0.50 and lexacc < 0.75:
            lexWa = 480
            lexWd = 475
        elif lexacc >=0.25 and lexacc < 0.50:
            lexWa = 470
            lexWd = 475
        elif lexacc >=0 and lexacc < 0.25:
            lexWa = 460
            lexWd = 475

        lexw_diff = lexWa - lexWd

        if lexw_diff > 31:
            lexRPI = '100/90'
            lexProficiency = 'Very Advanced'
            lextask_management = 'Extremely Easy'

        elif lexw_diff > 13 and lexw_diff < 31:
            lexRPI = '98/90 to 100/90'
            lexProficiency = 'Advanced'
            lextask_management = 'Very Easy'

        elif lexw_diff > 6 and lexw_diff < 14:
            lexRPI = '95/90 to 98/90'
            lexProficiency = 'Average to Advanced'
            lextask_management = 'Easy'

        elif lexw_diff > -6 and lexw_diff < 7:
            lexRPI = '82/90 to 95/90'
            lexProficiency = 'Average'
            lextask_management = 'Manageable'
            

        elif lexw_diff > -13 and lexw_diff < -7 :
            lexRPI = '67/90 to 82/90'
            lexProficiency = 'Limited to Average'
            lextask_management = 'Difficult'
            

        elif lexw_diff > -30 and lexw_diff < -14:
            lexRPI = '24/90 to 67/90'
            lexProficiency = 'Limited'
            lextask_management = 'Very Difficult'

        elif lexw_diff > -50 and lexw_diff < -31:
            lexRPI = '3/90 to 24/90'
            lexProficiency = 'Very Limited'
            lextask_management = 'Extremely Difficult'

        elif lexw_diff < -51:
            lexRPI = '0/90 to 3/90'
            lexProficiency = 'Extremely Limited'
            lextask_management = 'Nearly Impossible'

        print("W Difference is: ", lexw_diff)
        print("The Relative Proficiency Index for the student is: ", lexRPI),
        print("The Proficiency of child is: ", lexProficiency)
        print("The task management of the student is suggested to be: ", lextask_management)


        cursor.execute('INSERT INTO lex_result VALUES(%s,%s,%s,%s,%s)', [session['p_email'], session['s_name'], lexRPI, lexProficiency, lextask_management])
        mysql.connection.commit()
        return redirect(url_for('sections'))

     
    return render_template('end_test1.html')


@app.route('/feedback_dyscalculia', methods = ['GET', 'POST'])
def feedback_dyscalculia():
    name = session['s_name']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT total FROM cal_test WHERE p_email=%s',[session['p_email']])
    
    calacc1 = cursor.fetchone()
    cursor.execute('SELECT total FROM cal_test2 WHERE p_email=%s',[session['p_email']])
    calacc2 = cursor.fetchone()
    print(calacc1, calacc2)
    
    calacc = (float(calacc1['total'])*20+float(calacc2['total'])*18)/360
    calacc = round(calacc/2, 2)

    

    

    Wa = 0
    Wd = 0
    RPI = ''
    Proficiency = ''
    task_management = ''


    if calacc >= 0.75:
        Wa = 490
        Wd = 475
    elif calacc >=0.50 and calacc < 0.75:
        Wa = 480
        Wd = 475
    elif calacc >=0.25 and calacc < 0.50:
        Wa = 470
        Wd = 475
    elif calacc >=0 and calacc < 0.25:
        Wa = 460
        Wd = 475

    w_diff = Wa - Wd

    if w_diff > 31:
        RPI = '100/90'
        Proficiency = 'Very Advanced'
        task_management = 'Extremely Easy'

    elif w_diff > 13 and w_diff < 31:
        RPI = '98/90 to 100/90'
        Proficiency = 'Advanced'
        task_management = 'Very Easy'

    elif w_diff > 6 and w_diff < 14:
        RPI = '95/90 to 98/90'
        Proficiency = 'Average to Advanced'
        task_management = 'Easy'

    elif w_diff > -6 and w_diff < 7:
        RPI = '82/90 to 95/90'
        Proficiency = 'Average'
        task_management = 'Manageable'
        

    elif w_diff > -13 and w_diff < -7 :
        RPI = '67/90 to 82/90'
        Proficiency = 'Limited to Average'
        task_management = 'Difficult'
        

    elif w_diff > -30 and w_diff < -14:
        RPI = '24/90 to 67/90'
        Proficiency = 'Limited'
        task_management = 'Very Difficult'

    elif w_diff > -50 and w_diff < -31:
        RPI = '3/90 to 24/90'
        Proficiency = 'Very Limited'
        task_management = 'Extremely Difficult'

    elif w_diff < -51:
        RPI = '0/90 to 3/90'
        Proficiency = 'Extremely Limited'
        task_management = 'Nearly Impossible'

    cursor.execute('INSERT INTO cal_result VALUES(%s,%s,%s,%s,%s)', [session['p_email'],session['s_name'], RPI, Proficiency, task_management])
    mysql.connection.commit()
    if request.method == 'POST':
        ans1 = request.form['q1']
        ans2 = request.form['q2']
        ans3 = request.form['q3']
        ans4 = request.form.get('q4')
        print(ans1, ans2, ans3, ans4)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO feedback_dyscalculia VALUES(%s,%s,%s,%s,%s)',
                    [session['p_email'], ans1, ans2, ans3, ans4])
        mysql.connection.commit()
    
        return redirect(url_for('sections'))

    
    return render_template('end_test2.html')


@app.route('/feedback_dysgraphia', methods = ['GET', 'POST'])
def feedback_dysgraphia():
    name = session['s_name']
    if request.method == 'POST':
        ans1 = request.form['q1']
        ans2 = request.form['q2']
        ans3 = request.form['q3']
        ans4 = request.form.get('q4')
        print(ans1, ans2, ans3, ans4)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO feedback_dysgraphia VALUES(%s,%s,%s,%s,%s)',
                    [session['p_email'], ans1, ans2, ans3, ans4])
        mysql.connection.commit()


        return redirect(url_for('sections'))

    return render_template('end_test3.html')
  
@app.route('/feedback_adhd', methods = ['GET', 'POST'])
def feedback_adhd():
    name = session['s_name']
    if request.method == 'POST':
        ans1 = request.form['q1']
        ans2 = request.form['q2']
        ans3 = request.form['q3']
        ans4 = request.form.get('q4')
        print(ans1, ans2, ans3, ans4)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO feedback_adhd VALUES(%s,%s,%s,%s,%s)',
                    [session['p_email'], ans1, ans2, ans3, ans4])
        mysql.connection.commit()




        return redirect(url_for('sections'))

    return render_template('end_test4.html')




#DYSKEXIA SPEECH RECOGNITION


@app.route('/speechrblendwords')
def speechrblendwords():
    spoken_text = ''
    spoken_text1 = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM blending_words')
    para = cursor.fetchall()
    para_list = []
    for i in para:
        para_list.append(i['word'])
    for i in range(len(para_list)):
        para_list[i] = para_list[i].lower()
    orignal_text_list = para_list
    orignal_text = para_list
    

    with sr.Microphone() as source:
                audio_data = r.record(source, duration=5)
                print("Recognizing...")
                try :
                    spoken_text1= str(r.recognize_google(audio_data, language= "en-IN"))
                    spoken_text = spoken_text1.lower()
                    spoken_text = list(spoken_text.split(" "))
                    
                except :
                    pass

    
    print("Orignal Text: ", orignal_text)
    print('Spoken Text: ', spoken_text)
        
    right_words = []
    l1 = Counter(orignal_text)
    l2 = Counter(spoken_text)
    diff = l1 - l2
    print('og counter: ', l1)
    print('spoken counter: ', l2)
    print(diff)
    non_words = list(diff.elements())

    wrong_words = []
    for i in spoken_text:
        if i in orignal_text:
            right_words.append(i)
        else:
            wrong_words.append(i)

    print('right_words: ', right_words)
    print("Words child did not spoke which were in the actual sentence: ", non_words)
    print("Words pronounced by the child which were not in the actual sentence: ", wrong_words)
    



    score = len(right_words)/len(orignal_text_list)
    accuracy = len(right_words)/len(spoken_text)
    session['blendwords_accuracy'] = accuracy 
    print(session['blendwords_accuracy'])
    print(len(right_words))
    print(len(orignal_text_list))
    print(accuracy)

    # Next 4 lines used only for database purpose
    orignal_text = ' '.join(map(str, orignal_text))
    print('ogtext_list : ', orignal_text)
    spoken_text = ' '.join(map(str, spoken_text))
    print('spokentext_list : ', spoken_text)
    right_words = ' '.join(map(str, right_words))
    missing_words = ' '.join(map(str, non_words))
    extra_words = ' '.join(map(str, wrong_words))


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test_blendwords VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], orignal_text, spoken_text1, right_words,missing_words,extra_words, score, accuracy])
    mysql.connection.commit()
    return redirect(url_for('student_test_nonsensewords'))

@app.route('/speechrnonsensewords')
def speechrnonsensewords():
    spoken_text = ''
    spoken_text1 = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM nonsense_words')
    para = cursor.fetchall()
    para_list = []
    for i in para:
        para_list.append(i['word'])
    for i in range(len(para_list)):
        para_list[i] = para_list[i].lower()
    orignal_text_list = para_list
    orignal_text = para_list
    

    with sr.Microphone() as source:
                audio_data = r.record(source, duration=5)
                print("Recognizing...")
                try :
                    spoken_text1= str(r.recognize_google(audio_data, language= "en-IN"))
                    spoken_text = spoken_text1.lower()
                    spoken_text = list(spoken_text.split(" "))
                    
                except :
                    pass

    
    print("Orignal Text: ", orignal_text)
    print('Spoken Text: ', spoken_text)
        
    right_words = []
    l1 = Counter(orignal_text)
    l2 = Counter(spoken_text)
    diff = l1 - l2
    print('og counter: ', l1)
    print('spoken counter: ', l2)
    print(diff)
    non_words = list(diff.elements())

    wrong_words = []
    for i in spoken_text:
        if i in orignal_text:
            right_words.append(i)
        else:
            wrong_words.append(i)
    print('right_words: ', right_words)
    print("Words child did not spoke which were in the actual sentence: ", non_words)
    print("Words pronounced by the child which were not in the actual sentence: ", wrong_words)
    



    score = len(right_words)/len(orignal_text_list)
    accuracy = len(right_words)/len(spoken_text)
    session['nonsensewords_accuracy'] = accuracy 
    print(len(right_words))
    print(len(orignal_text_list))
    print(accuracy)

    # Next 4 lines used only for database purpose
    orignal_text = ' '.join(map(str, orignal_text))
    print('ogtext_list : ', orignal_text)
    spoken_text = ' '.join(map(str, spoken_text))
    print('spokentext_list : ', spoken_text)
    right_words = ' '.join(map(str, right_words))
    missing_words = ' '.join(map(str, non_words))
    extra_words = ' '.join(map(str, wrong_words))


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test_nonsensewords VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], orignal_text, spoken_text1, right_words,missing_words,extra_words,score, accuracy])

    
    mysql.connection.commit()
    return redirect(url_for('objects'))

@app.route('/speechrobjects')
def speechrobjects():
    spoken_text = ''
    spoken_text1 = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM objects')
    para = cursor.fetchall()
    para_list = []
    
    
    orignal_text = para_list
    for i in para:
        para_list.append(i['objects'])
    for i in range(len(para_list)):
        para_list[i] = para_list[i].lower()
    orignal_text_list = para_list
    objects = []
    for i in range(len(orignal_text)):
        objects.append(orignal_text[i].split())
    
    print(objects)
    orignal_text = objects[0]
    with sr.Microphone() as source:
                audio_data = r.record(source, duration=5)
                print("Recognizing...")
                try :
                    spoken_text1= str(r.recognize_google(audio_data, language= "en-IN"))
                    spoken_text = spoken_text1.lower()
                    spoken_text = list(spoken_text.split(" "))
                    
                except :
                    pass

    
    print("Orignal Text: ", orignal_text)
    print('Spoken Text: ', spoken_text)
        
    right_words = []
    l1 = Counter(orignal_text)
    l2 = Counter(spoken_text)
    diff = l1 - l2
    print('og counter: ', l1)
    print('spoken counter: ', l2)
    print(diff)
    non_words = list(diff.elements())

    wrong_words = []
    for i in spoken_text:
        if i in orignal_text:
            right_words.append(i)
        else:
            wrong_words.append(i)
    print('right_words: ', right_words)
    print("Words child did not spoke which were in the actual sentence: ", non_words)
    print("Words pronounced by the child which were not in the actual sentence: ", wrong_words)
    



    score = len(right_words)/len(orignal_text_list)
    if spoken_text!=0:
        accuracy = len(right_words)/len(spoken_text)
    session['objects_accuracy'] = accuracy 
    print(len(right_words))
    print(len(orignal_text))
    print(accuracy)

    # Next 4 lines used only for database purpose
    orignal_text = ' '.join(map(str, orignal_text))
    print('ogtext_list : ', orignal_text)
    spoken_text = ' '.join(map(str, spoken_text))
    print('spokentext_list : ', spoken_text)
    right_words = ' '.join(map(str, right_words))
    missing_words = ' '.join(map(str, non_words))
    extra_words = ' '.join(map(str, wrong_words))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test_objects VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], orignal_text, spoken_text1, right_words,missing_words,extra_words, score, accuracy])
    mysql.connection.commit()
    return redirect(url_for('student_test_word'))

@app.route('/speechrw')
def speechrw():
    spoken_text = ''
    spoken_text1 = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM words')
    para = cursor.fetchall()
    para_list = []
    for i in para:
        para_list.append(i['word'])
    for i in range(len(para_list)):
        para_list[i] = para_list[i].lower()
    orignal_text_list = para_list
    orignal_text = para_list
    

    with sr.Microphone() as source:
                audio_data = r.record(source, duration=5)
                print("Recognizing...")
                try :
                    spoken_text1= str(r.recognize_google(audio_data, language= "en-IN"))
                    spoken_text = spoken_text1.lower()
                    spoken_text = list(spoken_text.split(" "))
                    
                except :
                    pass

    
    print("Orignal Text: ", orignal_text)
    print('Spoken Text: ', spoken_text)
        
    right_words = []
    l1 = Counter(orignal_text)
    l2 = Counter(spoken_text)
    diff = l1 - l2
    print('og counter: ', l1)
    print('spoken counter: ', l2)
    print(diff)
    non_words = list(diff.elements())

    wrong_words = []
    for i in spoken_text:
        if i in orignal_text:
            right_words.append(i)
        else:
            wrong_words.append(i)
    print('right_words: ', right_words)
    print("Words child did not spoke which were in the actual sentence: ", non_words)
    print("Words pronounced by the child which were not in the actual sentence: ", wrong_words)
    



    score = len(right_words)/len(orignal_text_list)
    accuracy = len(right_words)/len(spoken_text)
    session['words_accuracy'] = accuracy 
    print(len(right_words))
    print(len(orignal_text_list))
    print(accuracy)

    # Next 4 lines used only for database purpose
    orignal_text = ' '.join(map(str, orignal_text))
    print('ogtext_list : ', orignal_text)
    spoken_text = ' '.join(map(str, spoken_text))
    print('spokentext_list : ', spoken_text)
    right_words = ' '.join(map(str, right_words))
    missing_words = ' '.join(map(str, non_words))
    extra_words = ' '.join(map(str, wrong_words))


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test_word VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], orignal_text, spoken_text1, right_words,missing_words,extra_words, score, accuracy])
    mysql.connection.commit()
    return redirect(url_for('student_test_sent'))

@app.route('/speechrs')
def speechrs():
    spoken_text = ''
    spoken_text1 = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM sentences')
    para = cursor.fetchall()

    para_list = []
    for i in para:
        para_list.append(i['sentence'])
    for i in range(len(para_list)):
        para_list[i] = para_list[i].lower()
    orignal_text_list = para_list
    orignal_text = para_list[0]
    orignal_text = str(orignal_text)
    orignal_text = orignal_text.split()
    name = str(session['s_name']).lower()
    orignal_text.append(name)
    

    with sr.Microphone() as source:
                audio_data = r.record(source, duration=5)
                print("Recognizing...")
                try :
                    spoken_text1= str(r.recognize_google(audio_data, language= "en-IN"))
                    spoken_text = spoken_text1.lower()
                    spoken_text = list(spoken_text.split(" "))
                    
                except :
                    pass

    
    print("Orignal Text: ", orignal_text)
    print('Spoken Text: ', spoken_text)
        
    right_words = []
    l1 = Counter(orignal_text)
    l2 = Counter(spoken_text)
    diff = l1 - l2
    print('og counter: ', l1)
    print('spoken counter: ', l2)
    print(diff)
    non_words = list(diff.elements())

    wrong_words = []
    for i in spoken_text:
        if i in orignal_text:
            right_words.append(i)
        else:
            wrong_words.append(i)
    print('right_words: ', right_words)
    print("Words child did not spoke which were in the actual sentence: ", non_words)
    print("Words pronounced by the child which were not in the actual sentence: ", wrong_words)
    



    score = len(right_words)/len(orignal_text_list)
    accuracy = len(right_words)/len(spoken_text)
    session['sent1_accuracy'] = accuracy 
    print(len(right_words))
    print(len(orignal_text))
    print(accuracy)

    # Next 4 lines used only for database purpose
    orignal_text = ' '.join(map(str, orignal_text))
    print('ogtext_list : ', orignal_text)
    spoken_text = ' '.join(map(str, spoken_text))
    print('spokentext_list : ', spoken_text)
    right_words = ' '.join(map(str, right_words))
    missing_words = ' '.join(map(str, non_words))
    extra_words = ' '.join(map(str, wrong_words))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test_sent VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], orignal_text, spoken_text1, right_words,missing_words,extra_words,score, accuracy])
    mysql.connection.commit()
    return redirect(url_for('student_test_sent1'))

@app.route('/speechrs1')
def speechrs1():
    spoken_text = ''
    spoken_text1 = ''
    school = 'school'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM sentences')
    para = cursor.fetchall()

    para_list = []
    for i in para:
        para_list.append(i['sentence'])
    for i in range(len(para_list)):
        para_list[i] = para_list[i].lower()
    orignal_text_list = para_list
    orignal_text = para_list[1]
    orignal_text = str(orignal_text)
    orignal_text = orignal_text.split()
    schoolname = str(session['school']).lower().split()
    for i in range(len(schoolname)):
       orignal_text.append(schoolname[i])
    orignal_text.append(school)
    

    with sr.Microphone() as source:
                audio_data = r.record(source, duration=5)
                print("Recognizing...")
                try :
                    spoken_text1= str(r.recognize_google(audio_data, language= "en-IN"))
                    spoken_text = spoken_text1.lower()
                    spoken_text = list(spoken_text.split(" "))
                    
                except :
                    pass

    
    print("Orignal Text: ", orignal_text)
    print('Spoken Text: ', spoken_text)
        
    right_words = []
    l1 = Counter(orignal_text)
    l2 = Counter(spoken_text)
    diff = l1 - l2
    print('og counter: ', l1)
    print('spoken counter: ', l2)
    print(diff)
    non_words = list(diff.elements())

    wrong_words = []
    for i in spoken_text:
        if i in orignal_text:
            right_words.append(i)
        else:
            wrong_words.append(i)
    print('right_words: ', right_words)
    print("Words child did not spoke which were in the actual sentence: ", non_words)
    print("Words pronounced by the child which were not in the actual sentence: ", wrong_words)
    



    score = len(right_words)/len(orignal_text_list)
    if spoken_text !=0:
        accuracy = len(right_words)/len(spoken_text)
    session['sent2_accuracy'] = accuracy 
    print(len(right_words))
    print(len(orignal_text))
    print(accuracy)

    # Next 4 lines used only for database purpose
    orignal_text = ' '.join(map(str, orignal_text))
    print('ogtext_list : ', orignal_text)
    spoken_text = ' '.join(map(str, spoken_text))
    print('spokentext_list : ', spoken_text)
    right_words = ' '.join(map(str, right_words))
    missing_words = ' '.join(map(str, non_words))
    extra_words = ' '.join(map(str, wrong_words))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test_sent VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], orignal_text, spoken_text1, right_words,missing_words,extra_words, score,accuracy])
    mysql.connection.commit()
    return redirect(url_for('student_test'))


@app.route('/speechr')
def speechr():
    spoken_text = ''
    spoken_text1 = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dys_identification')
    para = cursor.fetchall()
    para_list = []
    for i in para:
        para_list.append(i['para'])
    for i in range(len(para_list)):
        para_list[i] = para_list[i].lower()
    orignal_text_list = para_list[0]
    orignal_text = para_list[0]
    punc = '''!()-[]{};:'",<>./?@#$%^&*~'''

    for ele in orignal_text:
        if ele in punc:
         orignal_text = orignal_text.replace(ele, "")
    orignal_text = orignal_text.split()
    orignal_text = list(orignal_text)

    with sr.Microphone() as source:
                audio_data = r.record(source, duration=8)
                print("Recognizing...")
                try :
                    spoken_text1= str(r.recognize_google(audio_data, language= "en-IN"))
                    spoken_text = spoken_text1.lower()
                    spoken_text = list(spoken_text.split(" "))
                    
                except :
                    pass

    
    print("Orignal Text: ", orignal_text)
    print('Spoken Text: ', spoken_text)
        
    right_words = []
    l1 = Counter(orignal_text)
    l2 = Counter(spoken_text)
    diff = l1 - l2
    print('og counter: ', l1)
    print('spoken counter: ', l2)
    print(diff)
    non_words = list(diff.elements())

    wrong_words = []
    for i in spoken_text:
        if i in orignal_text:
            right_words.append(i)
        else:
            wrong_words.append(i)
    print('right_words: ', right_words)
    print("Words child did not spoke which were in the actual sentence: ", non_words)
    print("Words pronounced by the child which were not in the actual sentence: ", wrong_words)
    



    
    score = len(right_words)/len(orignal_text_list)
    accuracy = len(right_words)/len(spoken_text)
    session['para1_accuracy'] = accuracy 
    print(len(right_words))
    print(len(orignal_text))
    print(accuracy)

    # Next 4 lines used only for database purpose
    orignal_text = ' '.join(map(str, orignal_text))
    print('ogtext_list : ', orignal_text)
    spoken_text = ' '.join(map(str, spoken_text))
    print('spokentext_list : ', spoken_text)
    right_words = ' '.join(map(str, right_words))
    missing_words = ' '.join(map(str, non_words))
    extra_words = ' '.join(map(str, wrong_words))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test1 VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], orignal_text, spoken_text1, right_words,missing_words,extra_words,score, accuracy])
    mysql.connection.commit()
    
    return redirect(url_for('student_test1'))


@app.route('/speechr1')
def speechr1():
    spoken_text = ''
    spoken_text1 = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dys_identification')
    para = cursor.fetchall()
    para_list = []
    for i in para:
        para_list.append(i['para'])
    for i in range(len(para_list)):
        para_list[i] = para_list[i].lower()
    orignal_text_list = para_list[1]
    orignal_text = para_list[1]
    punc = '''!()-[]{};:'",<>./?@#$%^&*~'''

    for ele in orignal_text:
        if ele in punc:
         orignal_text = orignal_text.replace(ele, "")
    orignal_text = orignal_text.split()
    orignal_text = list(orignal_text)

    with sr.Microphone() as source:
                audio_data = r.record(source, duration=8)
                print("Recognizing...")
                try :
                    spoken_text1= str(r.recognize_google(audio_data, language= "en-IN"))
                    spoken_text = spoken_text1.lower()
                    spoken_text = list(spoken_text.split(" "))
                    
                except :
                    pass

    
    print("Orignal Text: ", orignal_text)
    print('Spoken Text: ', spoken_text)
        
    right_words = []
    l1 = Counter(orignal_text)
    l2 = Counter(spoken_text)
    diff = l1 - l2
    print('og counter: ', l1)
    print('spoken counter: ', l2)
    print(diff)
    non_words = list(diff.elements())

    wrong_words = []
    for i in spoken_text:
        if i in orignal_text:
            right_words.append(i)
        else:
            wrong_words.append(i)
    print('right_words: ', right_words)
    print("Words child did not spoke which were in the actual sentence: ", non_words)
    print("Words pronounced by the child which were not in the actual sentence: ", wrong_words)
    



    score = len(right_words)/len(orignal_text_list)
    accuracy = len(right_words)/len(spoken_text)
    session['para2_accuracy'] = accuracy 
    print(len(right_words))
    print(len(orignal_text))
    print(accuracy)

    # Next 4 lines used only for database purpose
    orignal_text = ' '.join(map(str, orignal_text))
    print('ogtext_list : ', orignal_text)
    spoken_text = ' '.join(map(str, spoken_text))
    print('spokentext_list : ', spoken_text)
    right_words = ' '.join(map(str, right_words))
    missing_words = ' '.join(map(str, non_words))
    extra_words = ' '.join(map(str, wrong_words))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO lex_test2 VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], orignal_text, spoken_text1, right_words,missing_words,extra_words,score, accuracy])
    mysql.connection.commit()
    return redirect(url_for('end_test1'))



#DYSLEXIA MODEL
def dyslexia_model():
    
    return None

#FEEDBACK PAGES

@app.route('/end_test1')
def end_test1():
    return render_template('end_test1.html')

@app.route('/end_test2')
def end_test2():
    return render_template('end_test2.html')

@app.route('/end_test3')
def end_test3():
    return render_template('end_test3.html')

@app.route('/end_test4')
def end_test4():
    return render_template('end_test4.html')



#DYSLEXIA ROUTES

@app.route('/student_test_blendingwords')
def student_test_blendingwords():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM blending_words')
    para = cursor.fetchall()
    name = session['s_name']
 
    return render_template('student_test_blendingwords.html',para=para, name=name)

@app.route('/student_test_nonsensewords')
def student_test_nonsensewords():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM nonsense_words')
    para = cursor.fetchall()
    name = session['s_name']
 
    return render_template('student_test_nonsensewords.html',para=para, name=name)


@app.route('/objects')
def objects():
    return render_template('objects.html')

@app.route('/student_test_word')
def student_test_word():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM words')
    para = cursor.fetchall()
    name = session['s_name']
 
    return render_template('student_test_word.html',para=para, name=name)

@app.route('/student_test_phrases')
def student_test_phrases():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dolce_phrases')
    para = cursor.fetchall()
 
    return render_template('student_test_phrases.html',para=para)

@app.route('/student_test_sent')
def student_test_sent():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM sentences')
    para = cursor.fetchall()
    print(para)
    name = session['s_name']
    return render_template('student_test_sent.html',para=para,s_name=name)

@app.route('/student_test_sent1')
def student_test_sent1():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM sentences')
    para = cursor.fetchall()
    print(para)
    
    schoolname = session['school']
    return render_template('student_test_sent1.html',para=para,schoolname=schoolname)

@app.route('/student_test')
def student_test():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dys_identification')
    para = cursor.fetchall()

    para_list = []
    for i in range(len(para)):
        x = para[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        para_list.append(list_h)
    return render_template('student_test.html',para_list=para_list)

@app.route('/student_test1')
def student_test1():
    text_og = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dys_identification')
    para = cursor.fetchall()

    para_list = []
    for i in range(len(para)):
        x = para[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        para_list.append(list_h)
    return render_template('student_test1.html',para_list=para_list)




@app.route('/list1')
def list1():
    return render_template('list1.html')


@app.route('/tables')
def tables():
    return render_template('tables.html')


@app.route('/common_test', methods=['GET', 'POST'])
def common_test():
    score = 0
    name = session['s_name']
    if request.method == 'POST' :
        option1 = request.form['q1']
        option2 = request.form['q2']
        option3 = request.form['q3']
        option4 = request.form['q4']
        option5 = request.form['q5']
        option6 = request.form['q6']
        option7 = request.form['q7']
        option8 = request.form['q8']
        option9 = request.form['q9']
        option10 = request.form['q10']
        option11 = request.form['q11']
        option12 = request.form['q12']
        option13 = request.form['q13']
        option14 = request.form['q14']
        option15 = request.form['q15']
        option16 = request.form['q16']
        option17 = request.form['q17']
        option18 = request.form['q18']

        
        if option1 == "7":
            score += 1
        if option2.lower() == "yes":
            score += 1
        if option3 == "5":
            score += 1
        if option4 == "20":
            score += 1
        if option5 == "18":
            score += 1
        if option6 == "16":
            score += 1
        if option7 == "6":
            score += 1
        if option8 == "11":
            score += 1
        if option9 == "10":
            score += 1
        if option10 == "4":
            score += 1
        if option11 == "60":
            score += 1
        if option12 == "4":
            score += 1
        if option13 == "2":
            score += 1    
        if option14 == "3":
            score += 1
        if option15 == "9":
            score += 1
        if option16 == "9":
            score += 1
        if option17 == "4":
            score += 1
        if option18 == "5":
            score += 1 

        print("Score:"+str(score))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO cal_test VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], option1, option2, option3, option4,option5,option6,option7,option8,option9,option10,option11,option12,option13,option14,option15,option16,option17,option18,score])
        mysql.connection.commit()
        return redirect(url_for('timer'))
    
    return render_template('common_test.html', name=name)

@app.route('/common_test2', methods=['GET', 'POST'])
def common_test2():
    score = 0
    name = session['s_name']
    if request.method == 'POST' :
        option1 = request.form['q1']
        option2 = request.form['q2']
        option3 = request.form['q3']
        option4 = request.form['q4']
        option5 = request.form['q5']
        option6 = request.form['q6']
        option7 = request.form['q7']
        option8 = request.form['q8']
        option9 = request.form['q9']
        option10 = request.form['q10']
        option11 = request.form['q11']
        option12 = request.form['q12']
        option13 = request.form['q13']
        option14 = request.form['q14']
        option15 = request.form['q15']
        option16 = request.form['q16']
        option17 = request.form['q17']
        option18 = request.form['q18']
        option19 = request.form['q19']
        option20 = request.form['q20']

        
        if option1 == "327":
            score += 1
        if option2 == "13":
            score += 1
        if option3 == "+":
            score += 1
        if option4 == "3":
            score += 1
        if option5 == "yes":
            score += 1
        if option6 == "98":
            score += 1
        if option7 == "21":
            score += 1
        if option8 == "0":
            score += 1
        if option9 == "9":
            score += 1
        if option10 == "7":
            score += 1
        if option11 == "7":
            score += 1
        if option12 == "13":
            score += 1
        if option13 == "8":
            score += 1    
        if option14 == "10":
            score += 1
        if option15 == "15":
            score += 1
        if option16 == "10":
            score += 1
        if option17 == "12":
            score += 1
        if option18 == "9":
            score += 1
        if option19 == "6":
            score += 1
        if option20 == "13":
            score += 1 

        print("Score:"+str(score))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO cal_test2 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                   [session['p_email'], option1, option2, option3, option4,option5,option6,option7,option8,option9,option10,option11,option12,option13,option14,option15,option16,option17,option18,option19,option20,score])
        mysql.connection.commit()
        return redirect(url_for('feedback_dyscalculia'))


    
    return render_template('common_test2.html', name=name)

@app.route('/timer')
def timer():
    return render_template('timer.html')

import os


#DYSGRAPHIA
@app.route('/dysgraphia_section1', methods=['GET', 'POST'])
def dysgraphia_section1():
    

    return render_template('dysgraphia_section1.html')

@app.route('/dysgraphia_section2', methods=['GET', 'POST'])
def dysgraphia_section2():
    if request.method == 'POST':
        file = request.files['filename']
        print(file)
        filename = secure_filename(file.filename)
        name= session['s_name']
        folders=os.listdir('F:\Codes\Python\dysgraphia')
        if name not in folders:
            os.mkdir('F:/Codes/Python/dysgraphia'+ '/' + name)
            UPLOAD_FOLDER = 'F:/Codes/Python/dysgraphia'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER + "/" + name
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            UPLOAD_FOLDER = 'F:/Codes/Python/dysgraphia'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER + "/" + name
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('feedback_dysgraphia'))
    return render_template('dysgraphia_section2.html')



        


@app.route('/adhd_section1', methods=['GET','POST'])
def adhd_section1():   
    if request.method=="POST" and "cam" in request.form: 
        global NAtt_timer, Att_timer, timerEnd, timerStart
        timerEnd, timerStart =  time.time(), time.time()
        NAtt_timer = 0
        pos = ''    
        face_model = get_face_detector()
        landmark_model = get_landmark_model()
        cap = cv2.VideoCapture(0)
        timerStart = time.time()
        ret, img = cap.read()
        size = img.shape
        font = cv2.FONT_HERSHEY_SIMPLEX 
        # 3D model points.
        model_points = np.array([
                                    (0.0, 0.0, 0.0),             # Nose tip
                                    (0.0, -330.0, -65.0),        # Chin
                                    (-225.0, 170.0, -135.0),     # Left eye left corner
                                    (225.0, 170.0, -135.0),      # Right eye right corne
                                    (-150.0, -150.0, -125.0),    # Left Mouth corner
                                    (150.0, -150.0, -125.0)      # Right mouth corner
                                ])

        # Camera internals
        focal_length = size[1]
        center = (size[1]/2, size[0]/2)
        camera_matrix = np.array(
                                [[focal_length, 0, center[0]],
                                [0, focal_length, center[1]],
                                [0, 0, 1]], dtype = "double"
                                )
        while True:
            ret, img = cap.read()
            if ret == True:
                faces = find_faces(img, face_model)
                for face in faces:
                    marks = detect_marks(img, landmark_model, face)
                    image_points = np.array([
                                            marks[30],     # Nose tip
                                            marks[8],     # Chin
                                            marks[36],     # Left eye left corner
                                            marks[45],     # Right eye right corne
                                            marks[48],     # Left Mouth corner
                                            marks[54]      # Right mouth corner
                                        ], dtype="double")
                    dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
                    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)
                    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
                    
                    p1 = ( int(image_points[0][0]), int(image_points[0][1]))
                    p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
                    rear_size = 1
                    rear_depth = 0
                    front_size = img.shape[1]
                    front_depth = front_size*2
                    val = [rear_size, rear_depth, front_size, front_depth]
                    point_3d = []
                    dist_coeffs = np.zeros((4,1))
                    rear_size = val[0]
                    rear_depth = val[1]
                    point_3d.append((-rear_size, -rear_size, rear_depth))
                    point_3d.append((-rear_size, rear_size, rear_depth))
                    point_3d.append((rear_size, rear_size, rear_depth))
                    point_3d.append((rear_size, -rear_size, rear_depth))
                    point_3d.append((-rear_size, -rear_size, rear_depth))
                    
                    front_size = val[2]
                    front_depth = val[3]
                    point_3d.append((-front_size, -front_size, front_depth))
                    point_3d.append((-front_size, front_size, front_depth))
                    point_3d.append((front_size, front_size, front_depth))
                    point_3d.append((front_size, -front_size, front_depth))
                    point_3d.append((-front_size, -front_size, front_depth))
                    point_3d = np.array(point_3d, dtype=np.float).reshape(-1, 3)
                    
                    # Map to 2d img points
                    (point_2d, _) = cv2.projectPoints(point_3d, rotation_vector,
                                                    translation_vector,
                                                    camera_matrix,
                                                    dist_coeffs)
                    point_2d = np.int32(point_2d.reshape(-1, 2))

                    x2 = (point_2d[5] + point_2d[8])//2
                    x1 = point_2d[2]

                    try:
                        m = (p2[1] - p1[1])/(p2[0] - p1[0])
                        ang1 = int(math.degrees(math.atan(m)))
                    except:
                        ang1 = 90
                    try:
                        m = (x2[1] - x1[1])/(x2[0] - x1[0])
                        ang2 = int(math.degrees(math.atan(-1/m)))
                    except:
                        ang2 = 90

                    if ang1 >= 48 or ang1 <= -48 or ang2 >= 48 or ang2 <= -48:
                        cv2.putText(img, 'Not Attentive', (90, 30), font, 2, (255, 255, 128), 3)
                        NAtt_timer += 0.1
                    else:
                        cv2.putText(img, 'Attentive', (90, 30), font, 2, (255, 255, 128), 3)
                        pos = 'A'
                cv2.imshow('img', img)
                timerEnd = time.time()
                Total_time = timerEnd - timerStart
                # if Total_time == 20:
                #     break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    timerEnd = time.time()
                    Total_time = timerEnd - timerStart
                    break  
                if Total_time > 50:
                    print("Total time: " + str((Total_time)))
                    print("Distraction Time: " + str(NAtt_timer))
                    print("Attention Time: " + str((Total_time - NAtt_timer)))
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('INSERT INTO adhd_time VALUES(%s,%s,%s,%s)',
                    [session['p_email'],Total_time - NAtt_timer, NAtt_timer, Total_time])
                    mysql.connection.commit()
                    break      
            
        cv2.destroyAllWindows()
        cap.release()
    return render_template('adhd_section1.html')

@app.route('/adhd_questions', methods=['GET', 'POST'])
def adhd_questions():
    score = 0
    if request.method == 'POST':
        option1 = request.form['q1']
        option2 = request.form['q2']
        option3 = request.form['q3']
        option4 = str(request.form['q4'])    
  
        if option1 == "bread" or option1 == "Bread":
            score += 1
            print(score)
        if option2 == "no" or option2 == "No":
            score += 1
            print(score)
        if option3 == "Monkey" or option3 == 'monkey':
            score += 1
            print(score)
        
        og_text = 'We must learn to share what we have'
        doc1 = nlp(og_text)
        doc2 = nlp(option4)
        print(doc1.similarity(doc2)) 
        if doc1.similarity(doc2) > 0.40:
            score +=1
        print(option1, option2, option3, option4)
        print(score)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO adhd_test VALUES(%s,%s,%s,%s,%s,%s)',
                    [session['p_email'], option1, option2, option3, option4, score])
        mysql.connection.commit()
        return redirect(url_for('adhd_section2'))
    return render_template('adhd_questions.html')    

@app.route('/adhd_section2', methods=['GET', 'POST'])
def adhd_section2():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM adhd_test WHERE p_email = %s ', [session['p_email']])
    test = cursor.fetchone()
    cursor.execute('SELECT * FROM adhd_time WHERE p_email = %s ', [session['p_email']])
    time = cursor.fetchone()   
    avg= ((float(time['dist_time'])*4) + (4-float(test['total']))*300)/1200
    avg = avg/2
    print(avg)

    Wa = 0
    Wd = 0
    RPI = ''
    Proficiency = ''
    task_management = ''


    if avg >= 0.75:
        Wa = 490
        Wd = 475
    elif avg >=0.50 and avg < 0.75:
        Wa = 480
        Wd = 475
    elif avg >=0.25 and avg < 0.50:
        Wa = 470
        Wd = 475
    elif avg >=0 and avg < 0.25:
        Wa = 460
        Wd = 475

    w_diff = Wa - Wd

    if w_diff > 31:
        RPI = '100/90'
        Proficiency = 'Very Advanced'
        task_management = 'Extremely Easy'

    elif w_diff > 13 and w_diff < 31:
        RPI = '98/90 to 100/90'
        Proficiency = 'Advanced'
        task_management = 'Very Easy'

    elif w_diff > 6 and w_diff < 14:
        RPI = '95/90 to 98/90'
        Proficiency = 'Average to Advanced'
        task_management = 'Easy'

    elif w_diff > -6 and w_diff < 7:
        RPI = '82/90 to 95/90'
        Proficiency = 'Average'
        task_management = 'Manageable'
        

    elif w_diff > -13 and w_diff < -7 :
        RPI = '67/90 to 82/90'
        Proficiency = 'Limited to Average'
        task_management = 'Difficult'
        

    elif w_diff > -30 and w_diff < -14:
        RPI = '24/90 to 67/90'
        Proficiency = 'Limited'
        task_management = 'Very Difficult'

    elif w_diff > -50 and w_diff < -31:
        RPI = '3/90 to 24/90'
        Proficiency = 'Very Limited'
        task_management = 'Extremely Difficult'

    elif w_diff < -51:
        RPI = '0/90 to 3/90'
        Proficiency = 'Extremely Limited'
        task_management = 'Nearly Impossible'

    

    cursor.execute('INSERT INTO adhd_result VALUES(%s,%s,%s,%s,%s)', [session['p_email'],session['s_name'], RPI, Proficiency, task_management])
    mysql.connection.commit()
    
    
    if request.method=="POST":
        return redirect(url_for('feedback_adhd'))
    return render_template('adhd_section2.html')



#PARENTS LOGIN

@app.route('/p_login', methods=['GET', 'POST'])
def p_login():
    if request.method == 'POST':
       
        # Create variables for easy access
        p_email = request.form['p_email']
        p_pass = request.form['password']
       
        # Check if account exists using MySQL

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM p_creds WHERE p_email = %s ', [p_email])
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            session['p_name']=account['p_name']
            session['s_name']=account['s_name']
            session['p_email']=account['p_email']            
            return redirect(url_for('parent_profile'))
            # account exists and test NOT taken, so redirect to exam page page
    return render_template('p_login.html')

@app.route('/parent_profile', methods=['GET','POST'])
def parent_profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM p_creds WHERE p_email=%s', [session['p_email']])
    para = cursor.fetchone()
    
    return render_template('parent_profile.html',para=para)


#STUDENT PROFILE

@app.route('/<s_name>', methods=['GET','POST'])
def s_name(s_name):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT s_name,school,p_email FROM p_creds WHERE s_name=%s',[s_name])
    account=cursor.fetchone()

    cursor.execute('SELECT * FROM dys_parent_test WHERE p_email=%s', [account['p_email']])
    account1 =cursor.fetchone()
    questions=['Q.1 Is the child able to cope up with the reading according to his/her grade level ?', 'Q.2 Is the child able to read common printed words ?','Q.3 Is the child able to pronounce the words correctly ?','Q.4 Is the child able to understand what he/she reads ?','Q.5 Is the child able to read without skipping lines and omitting words ?','Q.6 Rate the memory of child.','Q.7 Is the child able to recall past events ?',"Q.8 How is child's semantic skills ?","Q.9 Rate the spelling formation of child.","Q.10 Is the child able to get correct answer of same question twice ?","Q.11 Is the child able to solve the numeracy questions ?i.e. count or make connection with words","Q.12 Is the child able to recognize and write numbers and tell the sequence of the numbers ?","Q.13 Is the child able to do addition, subtraction, multiplication and division ?","Q.14 Is the child able to sort numbers and items having common characteristics ?","Q.15 Is the child able to compare objects having contrasting behavior ?"]
    del account1['p_email']
    for i in account1:
        if account1[i]==0:
            account1[i]="Poor"
        elif account1[i]==1:
            account1[i]="Good"
        elif account1[i]==2:
            account1[i]="Excellent"
    account2={}
    for (i,j) in zip(account1.keys(),questions):
        account2[j]=account1[i]
    

    
    cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_word WHERE p_email=%s',[account['p_email']])
    word=cursor.fetchone()

    cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_sent WHERE p_email=%s',[account['p_email']])
    sent=cursor.fetchall()

    cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test1 WHERE p_email=%s',[account['p_email']])
    para=cursor.fetchone()

    cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test2 WHERE p_email=%s',[account['p_email']])
    para2=cursor.fetchone()

    cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_objects WHERE p_email=%s',[account['p_email']])
    obj=cursor.fetchone()

    cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_nonsensewords WHERE p_email=%s',[account['p_email']])
    nonwords=cursor.fetchone()

    cursor.execute('SELECT given,spoken,accuracy,missing_words,extra_words FROM lex_test_blendwords WHERE p_email=%s',[account['p_email']])
    blend=cursor.fetchone()

    cursor.execute('SELECT total FROM cal_test WHERE p_email=%s',[account['p_email']])
    calacc1 = cursor.fetchone()
    cursor.execute('SELECT total FROM cal_test2 WHERE p_email=%s',[account['p_email']])
    calacc2 = cursor.fetchone()
    print(calacc1, calacc2)
    
    calacc = (float(calacc1['total'])*20+float(calacc2['total'])*18)/360
    calacc = round(calacc/2, 2)

    

    

    Wa = 0
    Wd = 0
    RPI = ''
    Proficiency = ''
    task_management = ''


    if calacc >= 0.75:
        Wa = 490
        Wd = 475
    elif calacc >=0.50 and calacc < 0.75:
        Wa = 480
        Wd = 475
    elif calacc >=0.25 and calacc < 0.50:
        Wa = 470
        Wd = 475
    elif calacc >=0 and calacc < 0.25:
        Wa = 460
        Wd = 475

    w_diff = Wa - Wd

    if w_diff > 31:
        RPI = '100/90'
        Proficiency = 'Very Advanced'
        task_management = 'Extremely Easy'

    elif w_diff > 13 and w_diff < 31:
        RPI = '98/90 to 100/90'
        Proficiency = 'Advanced'
        task_management = 'Very Easy'

    elif w_diff > 6 and w_diff < 14:
        RPI = '95/90 to 98/90'
        Proficiency = 'Average to Advanced'
        task_management = 'Easy'

    elif w_diff > -6 and w_diff < 7:
        RPI = '82/90 to 95/90'
        Proficiency = 'Average'
        task_management = 'Manageable'
        

    elif w_diff > -13 and w_diff < -7 :
        RPI = '67/90 to 82/90'
        Proficiency = 'Limited to Average'
        task_management = 'Difficult'
        

    elif w_diff > -30 and w_diff < -14:
        RPI = '24/90 to 67/90'
        Proficiency = 'Limited'
        task_management = 'Very Difficult'

    elif w_diff > -50 and w_diff < -31:
        RPI = '3/90 to 24/90'
        Proficiency = 'Very Limited'
        task_management = 'Extremely Difficult'

    elif w_diff < -51:
        RPI = '0/90 to 3/90'
        Proficiency = 'Extremely Limited'
        task_management = 'Nearly Impossible'

    print("W Difference is: ", w_diff)
    print("The Relative Proficiency Index for the student is: ", RPI),
    print("The Proficiency of child is: ", Proficiency)
    print("The task management of the student is suggested to be: ", task_management)


    cursor.execute('INSERT INTO cal_result VALUES(%s,%s,%s,%s,%s)', [session['p_email'],session['s_name'], RPI, Proficiency, task_management])
    mysql.connection.commit()

    cs_score=0
    score=0
    mf_score=0
    qr_score=0
    q1=0
    q2=0
    q3=0
    q4=0
    q5=0
    q6=0
    q7=0
    q8=0
    q9=0
    q10=0
    q11=0
    q12=0
    q13=0
    q14=0
    q15=0
    q16=0
    q17=0
    q18=0
    aq1=0
    aq2=0
    aq3=0
    aq4=0
    aq5=0
    aq6=0
    aq7=0
    aq8=0
    aq9=0
    aq10=0
    aq11=0
    aq12=0
    aq13=0
    aq14=0
    aq15=0
    aq16=0
    aq17=0
    aq18=0
    aq19=0
    aq20=0
    cursor.execute('SELECT * FROM cal_test WHERE p_email=%s',[account['p_email']])
    cal_res=cursor.fetchone()
    if cal_res['q1'] == "7":
            cs_score += 1
            q1 = 1
    if cal_res['q2'].lower() == "yes":
            cs_score += 1
            q2 = 1
    if cal_res['q3'] == "5":
            cs_score += 1
            q3 = 1
    if cal_res['q4'] == "20":
            cs_score += 1
            q4 = 1
    if cal_res['q5'] == "18":
            cs_score += 1
            q5 = 1
    if cal_res['q6'] == "16":
            cs_score += 1
            q6 = 1
    if cal_res['q7'] == "6":
            cs_score += 1
            q7 = 1
    if cal_res['q8'] == "11":
            cs_score += 1
            q8 = 1
    if cal_res['q9'] == "10":
            cs_score += 1
            q9 = 1
    if cal_res['q10'] == "4":
            cs_score += 1
            q10 = 1
    if cal_res['q11'] == "60":
            score += 1
            q11 = 1
    if cal_res['q12'] == "4":
            score += 1
            q12 = 1
    if cal_res['q13'] == "2":
            score += 1 
            q13 = 1   
    if cal_res['q14'] == "3":
            score += 1
            q14 = 1
    if cal_res['q15'] == "9":
            score += 1
            q15 = 1
    if cal_res['q16'] == "9":
            score += 1
            q16 = 1
    if cal_res['q17'] == "4":
            score += 1
            q17 = 1
    if cal_res['q18'] == "5":
            score += 1
            q18 = 1
    
    

    cursor.execute('SELECT * FROM cal_test2 WHERE p_email=%s',[account['p_email']])
    cal_res2=cursor.fetchone()
    if cal_res2['q1'] == "327":
            mf_score += 1
            aq1 = 1
    if cal_res2['q2'] == "13":
            mf_score += 1
            aq2 = 1
    if cal_res2['q3'] == "+":
            mf_score += 1
            aq3 = 1
    if cal_res2['q4'] == "3":
            mf_score += 1
            aq4 = 1
    if cal_res2['q5'] == "yes":
            mf_score += 1
            aq5 = 1
    if cal_res2['q6'] == "98":
            mf_score += 1
            aq6 = 1
    if cal_res2['q7'] == "21":
            mf_score += 1
            aq7 = 1
    if cal_res2['q8'] == "0":
            mf_score += 1
            aq8 = 1
    if cal_res2['q9'] == "9":
            mf_score += 1
            aq9 = 1
    if cal_res2['q10'] == "7":
            mf_score += 1
            aq10 = 1
    if cal_res2['q11'] == "7":
            mf_score += 1
            aq11 = 1
    if cal_res2['q12'] == "13":
            qr_score += 1
            aq12 = 1
    if cal_res2['q13'] == "8":
            qr_score += 1 
            aq13 = 1   
    if cal_res2['q14'] == "10":
            qr_score += 1
            aq14 = 1
    if cal_res2['q15'] == "15":
            qr_score += 1
            aq15 = 1
    if cal_res2['q16'] == "10":
            qr_score += 1
            aq16 = 1
    if cal_res2['q17'] == "12":
            qr_score += 1
            aq17 = 1
    if cal_res2['q18'] == "9":
            qr_score += 1
            aq18 = 1
    if cal_res2['q19'] == "6":
            qr_score += 1
            aq19 = 1
    if cal_res2['q20'] == "13":
            qr_score += 1 
            aq20 = 1

    
    #ADHD
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
            'SELECT * FROM adhd_test WHERE p_email = %s ', [account['p_email']])
    test = cursor.fetchone()
    
    cursor.execute(
            'SELECT * FROM adhd_time WHERE p_email = %s ', [account['p_email']])
    time = cursor.fetchone()
    print(test,time,'aaaaaa')



    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM lex_result WHERE s_name=%s',[s_name]) 
    lex = cursor.fetchone() 
    cursor.execute('SELECT * FROM cal_result WHERE s_name=%s',[s_name])  
    cal = cursor.fetchone() 
    cursor.execute('SELECT * FROM adhd_result WHERE s_name=%s',[s_name]) 
    adhd = cursor.fetchone()    
    lexrpi = lex['rpi']
    lexprof = lex['prof']
    leximp = lex['implications']

    calrpi = cal['rpi']
    calprof = cal['prof']
    calimp = cal['implications']

    adrpi = adhd['rpi']
    adprof = adhd['prof']
    adimp = adhd['implications']
    
    if request.method=="POST":
        pdf = FPDF()
        pdf.add_page()

        

        pdf.set_font('helvetica', size=11)
        pdf.cell(200,20, txt='Cognitive Analysis Report', ln=1, align='C')
        pdf.text( 20,45, f'Name of Student: {s_name}')
        pdf.text( 70,30, 'Specific Learning Disability Assesment Score')
        pdf.text( 80,50, "Reading Disability - Dyslexia:")

        pdf.text( 20,65, f'Relative Proficiency Index of student - {lexrpi}')
        pdf.text( 20,70, f'Proficiency of student is - {lexprof}')
        pdf.text( 20,75, f'Task Management skills of student is - {leximp}')

       



        pdf.text(85, 135, "Maths Disability - Dyscalculia:")
        pdf.text( 20,145, f'Relative Proficiency Index of student - {calrpi}')
        pdf.text( 20,150, f'Proficiency of student is - {calprof}')
        pdf.text( 20,155, f'Task Management skills of student is - {calimp}')
        
        



        pdf.text(80, 215, "Handwriting Disability - Dysgraphia:")
        pdf.text( 20,225, f'Relative Proficiency Index of student - {adrpi}')
        pdf.text( 20,230, f'Proficiency of student is - {adprof}')
        pdf.text( 20,235, f'Task Management skills of student is - {adimp}')
        


        pdf.add_page()
        pdf.text(80, 30, "Attention Deficit Hyperactivity Disorder")
        pdf.text( 20,40, f'Relative Proficiency Index of student - {RPI}')
        pdf.text( 20,45, f'Proficiency of student is -{Proficiency} ')
        pdf.text( 20,50, f'Task Management skills of student is - {task_management}')
       



        pdf.output('LD.pdf')  

    



    return render_template('student_profile1.html',account=account, account1=account2,word=word,sent=sent,para=para,para2=para2,obj=obj,nonwords=nonwords,blend=blend,cs_marks=cs_score,marks=score,mf_marks=mf_score,qr_marks=qr_score,time=time,test=test)


    
if __name__ == "__main__":
    app.run(debug=True)