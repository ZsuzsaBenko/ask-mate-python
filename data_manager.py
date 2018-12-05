# This module handles all the data received from the user.

import time
import connection
import util
import os


question_headers = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_headers = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def convert_questions_data():
    questions = connection.read_csv_file("sample_data/question.csv", question_headers)
    for question in questions:
        question["id"] = int(question["id"])
        question["submission_time"] = util.convert_timestamp_to_date(question["submission_time"])
        question["view_number"] = int(question["view_number"])
        question["vote_number"] = int(question["vote_number"])
    return questions


def sort_questions(questions, order_by=None, order_direction=None):
    if not order_by and not order_direction or order_by == "submission_time" and order_direction == "desc":
        questions = sorted(questions, key=lambda k: k["submission_time"], reverse=True)
    elif order_by == "submission_time" and order_direction == "asc":
        questions = sorted(questions, key=lambda k: k["submission_time"])
    elif order_by == "view_number" and order_direction == "desc":
        questions = sorted(questions, key=lambda k: k["view_number"], reverse=True)
    elif order_by == "view_number" and order_direction == "asc":
        questions = sorted(questions, key=lambda k: k["view_number"])
    elif order_by == "vote_number" and order_direction == "desc":
        questions = sorted(questions, key=lambda k: k["vote_number"], reverse=True)
    elif order_by == "vote_number" and order_direction == "asc":
        questions = sorted(questions, key=lambda k: k["vote_number"])
    elif order_by == "title" and order_direction == "asc":
        questions = sorted(questions, key=lambda k: k["title"])
    elif order_by == "title" and order_direction == "desc":
        questions = sorted(questions, key=lambda k: k["title"], reverse=True)
    return questions


def convert_answers_data():
    answers = connection.read_csv_file("sample_data/answer.csv", answer_headers)
    for answer in answers:
        answer["id"] = int(answer["id"])
        answer["submission_time"] = util.convert_timestamp_to_date(answer["submission_time"])
        answer["vote_number"] = int(answer["vote_number"])
        answer["question_id"] = int(answer["question_id"])
    return answers


def add_new_question(item_data):
    new_question = {}
    questions = connection.read_csv_file("sample_data/question.csv", question_headers)
    new_question["id"] = util.generate__id(questions)
    new_question["submission_time"] = str(int(time.time()))
    new_question["view_number"] = 0
    new_question["vote_number"] = 0
    new_question["title"] = item_data["title"]
    new_question["message"] = item_data["message"]
    new_question["image"] = item_data["image"]
    questions.append(new_question)
    connection.write_csv_file("sample_data/question.csv", questions, question_headers)
    return new_question["id"]


def delete_answer(id):
    answers = connection.read_csv_file("sample_data/answer.csv", answer_headers)
    for answer in answers:
        if id == answer["id"]:
            if answer["image"] != '':
                image = "static/" + answer["image"]
                os.remove(image)
            answers.remove(answer)
    connection.write_csv_file("sample_data/answer.csv", answers, answer_headers)


def delete_question(id):
    answers = connection.read_csv_file("sample_data/answer.csv", answer_headers)
    questions = connection.read_csv_file("sample_data/question.csv", question_headers)
    for question in questions:
        if id == question["id"]:
            if question["image"] != '':
                image = "static/" + question["image"]
                os.remove(image)
            questions.remove(question)
    for answer in answers:
        if id == answer["question_id"]:
            if answer["image"] != '':
                image = "static/" + answer["image"]
                os.remove(image)
            answers.remove(answer)
    connection.write_csv_file("sample_data/answer.csv", answers, answer_headers)
    connection.write_csv_file("sample_data/question.csv", questions, question_headers)


def add_new_answer(item_data):
    new_answer = {}
    answers = connection.read_csv_file("sample_data/answer.csv", answer_headers)
    new_answer["id"] = util.generate__id(answers)
    new_answer["submission_time"] = str(int(time.time()))
    new_answer["vote_number"] = 0
    new_answer["question_id"] = item_data["question_id"]
    new_answer["message"] = item_data["message"]
    new_answer["image"] = item_data["image"]
    answers.append(new_answer)
    connection.write_csv_file("sample_data/answer.csv", answers, answer_headers)
    return new_answer["id"]

