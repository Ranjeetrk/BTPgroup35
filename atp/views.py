""" 
@Author: Kumar Nityan Suman
@Date: 2018-05-15 10:00:33
@Last Modified time: 2019-01-19 16:34:33
"""

# import flask dependencies
import os
import click
import flask
from datetime import datetime
from flask import render_template, request
from werkzeug import secure_filename
from atp import app

# import app logic files
from atp.article import Article
from atp.subjective_question import generate_subj_question
from atp.cosine_similarity import evaluate_subj_answer
from atp.util import generate_trivia,generate_trivia_2,generate_trivia_3, get_obj_question, get_sbj_question
from atp.util import relative_ranking, back_up_data
# import important libraries
import pandas as pd
import numpy as np

# global data holder
global_name_list = list()
global_answer_list = list()
global_test_id = list()
global_user_answer_list=list()
global_question_list=list()


@app.route('/')
@app.route('/home')
def home():
    ''' Renders the home page '''
    return render_template(
        "index.html",
        date=datetime.now().day,
        month=datetime.now().month,
        year=datetime.now().year
        )


@app.route("/form", methods=['GET', 'POST'])
def form():
    ''' prompt for user to start procedure of test '''
    global_name_list.clear()
    global_name_list.clear()
    global_answer_list.clear()
    global_test_id.clear()
    global_test_id.clear()
    user_name = request.form["username"]
    if user_name == "":
        user_name = "Admin"
    
    global_name_list.append(user_name)

    return render_template(
        "form.html",
        username=user_name
        )


@app.route("/generate_test", methods=['GET', 'POST'])
def generate_test():
    # get subject id
    subject_id = request.form["subject_id"]
    filename = ""
    if subject_id == "1":
        global_name_list.append("Software Testing")
        filename = str(os.getcwd()) + "/sample_test_data/software-testing.txt"
        print(filename)
    elif subject_id == "2":
        global_name_list.append("DBMS")
        filename = str(os.getcwd()) + "/sample_test_data/dbms.txt"
    elif subject_id == "3":
        global_name_list.append("ML")
        filename = str(os.getcwd()) + "/sample_test_data/ml.txt"
    else:
        # file containing data to generate test
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(secure_filename(file.filename))
        global_name_list.append("Sample Test")
    
    # get test type id
    test_id = request.form["test_id"]
    global_test_id.append(test_id)

    if test_id == "1":
        # generate word/phrase question
        que_ans_pair = generate_trivia(filename)
        # get generated question and answer at random
        question_list, answer_list = get_obj_question(que_ans_pair)
        global_answer_list.clear()
        global_question_list.clear()
        for indi_ans in answer_list:
            global_answer_list.append(indi_ans)
        for indi_ques in question_list:
            global_question_list.append(indi_ques)

        return render_template(
        "give_test.html",
        username=global_name_list[0],
        testname=global_name_list[1],
        question1=question_list[0],
        question2=question_list[1],
        question3=question_list[2],
        question4=question_list[3],
        question5=question_list[4],
        question6=question_list[5]        
        )
    elif test_id == "2":
        # generate word/phrase question
        que_ans_pair = generate_trivia_2(filename)
        # get generated question and answer at random
        question_list, answer_list = get_obj_question(que_ans_pair)
        global_answer_list.clear()
        global_question_list.clear()
        for indi_ans in answer_list:
            global_answer_list.append(indi_ans)
        for indi_ques in question_list:
            global_question_list.append(indi_ques)


        return render_template(
        "give_test.html",
        username=global_name_list[0],
        testname=global_name_list[1],
        question1=question_list[0],
        question2=question_list[1],
        question3=question_list[2],
        question4=question_list[3],
        question5=question_list[4],
        question6=question_list[5]        
        )   
    elif test_id == "3":
        # generate word/phrase question
        que_ans_pair = generate_trivia_3(filename)
        # get generated question and answer at random
        question_list, answer_list = get_obj_question(que_ans_pair)
        global_answer_list.clear()
        global_question_list.clear()
        for indi_ans in answer_list:
            global_answer_list.append(indi_ans)
        for indi_ques in question_list:
            global_question_list.append(indi_ques)


        return render_template(
        "give_test.html",
        username=global_name_list[0],
        testname=global_name_list[1],
        question1=question_list[0],
        question2=question_list[1],
        question3=question_list[2],
        question4=question_list[3],
        question5=question_list[4],
        question6=question_list[5]

        )   
    elif test_id=="4":
        # generate subjective question
        que_ans_pair = generate_subj_question(filename)
        # get one of the generated question and answer at random
        question_list, answer_list = get_sbj_question(que_ans_pair)
        global_answer_list.clear()
        global_question_list.clear()
        for indi_ans in answer_list:
            global_answer_list.append(indi_ans)
        for indi_ques in question_list:
            global_question_list.append(indi_ques)


        return render_template(
        "give_test_2.html",
        username=global_name_list[0],
        testname=global_name_list[1],
        question1=question_list[0],
        question2=question_list[1]
        )


@ app.route("/output", methods=["GET", "POST"])
def output():
    # give result based on the test taken by the user
    user_ans = list()
    if global_test_id[0] != "4":
        # get objective test user responses
        temp = request.form["answer1"]
        temp = str(temp).strip(" ")
        user_ans.append(temp.upper())

        temp = request.form["answer2"]
        temp = str(temp).strip(" ")
        user_ans.append(temp.upper())

        temp = request.form["answer3"]
        temp = str(temp).strip(" ")
        user_ans.append(temp.upper())

        temp = request.form["answer4"]
        temp = str(temp).strip(" ")
        user_ans.append(temp.upper())

        temp = request.form["answer5"]
        temp = str(temp).strip(" ")
        user_ans.append(temp.upper())

        temp = request.form["answer6"]
        temp = str(temp).strip(" ")
        user_ans.append(temp.upper())
    else:
        # subjective test user responses
        temp = request.form["answer1"]
        temp = str(temp).strip(" ")
        user_ans.append(temp.upper())

        temp = request.form["answer2"]
        temp = str(temp).strip(" ")
        user_ans.append(temp.upper())

        # save user answer to globle useranser list
    # global_user_answer_list=user_ans

    # get the default answer for the question
    default_ans = list()
    for x in global_answer_list:
        x = str(x)
        x = x.strip(" ")
        x = x.upper()
        default_ans.append(x)
    for y in user_ans:
        y = str(y)
        y = y.strip(" ")
        y = y.upper()
        global_user_answer_list.append(y)

    username = global_name_list[0]
    subjectname = global_name_list[1]
    
    # evaluate the user repsonse
    total_score = 0
    flag = ""
    if global_test_id[0] == "4":
        flag = "2"
        # evaluate subjective answer
        for i in range(len(default_ans)):
            total_score += evaluate_subj_answer(default_ans[i], user_ans[i])
        total_score /= 2
        total_score = round(total_score, 3)
        # back up the user details and score for rank analysis
        status = "Score Not Saved!"
        if back_up_data(username, subjectname, total_score, "2") == True:
            status = "Score Saved!"
    else:
        flag = "1"
        # evaluate objective answer
        for i in range(len(user_ans)):
            if user_ans[i] == default_ans[i]:
                total_score += 100
        total_score /= 6
        total_score = round(total_score, 3)
        # back up the user details and score for rank analysis
        status = "Score Not Saved!"
        if back_up_data(username, subjectname, total_score, "1") == True:
            status = "Score Saved!"

    max_score, mean_score, min_score = relative_ranking(subjectname, flag)

    # clear the global variables for the next instance
    # global_name_list.clear()
    # global_answer_list.clear()
    # global_test_id.clear()
    # global_test_id.clear()
    user_ans.clear()
    default_ans.clear()

    return render_template(
        "output.html",
        show_score=total_score,
        username=username,
        subjectname=subjectname,
        status=status,
        max_score=max_score,
        mean_score=mean_score,
        min_score=min_score
    )
# end of the application

@ app.route("/question_answer", methods=["GET", "POST"])
def question_answer():
    # give result based on the test taken by the user
    

    # get the default answer for the question

    username = global_name_list[0]
    subjectname = global_name_list[1]
    # # get test type id
    # test_id = request.form["test_id"]
    # global_test_id.append(test_id)

    if global_test_id[0] != "4":
        return render_template(
            "question_answer.html",
            username=global_name_list[0],
            testname=global_name_list[1],
            ques1=global_question_list[0],
            ques2=global_question_list[1],
            ques3=global_question_list[2],
            ques4=global_question_list[3],
            ques5=global_question_list[4],
            ques6=global_question_list[5],
            ans1=global_answer_list[0],       
            ans2=global_answer_list[1],       
            ans3=global_answer_list[2],       
            ans4=global_answer_list[3],       
            ans5=global_answer_list[4],       
            ans6=global_answer_list[5],
            # user_ans1=global_user_answer_list[0],
            # user_ans2=global_user_answer_list[1],
            # user_ans3=global_user_answer_list[2],
            # user_ans4=global_user_answer_list[3],
            # user_ans5=global_user_answer_list[4],
            # user_ans6=global_user_answer_list[5]
            )
    else:
        global_name_list.clear()
        global_name_list.clear()
        global_answer_list.clear()
        global_test_id.clear()
        global_test_id.clear()

    
    # clear the global variables for the next instance

