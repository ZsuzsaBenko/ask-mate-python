# This module handles all the data received from the user.

import time
import connection
import util


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

