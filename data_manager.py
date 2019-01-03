# This module handles all the data received from the user.

import os
import time
import connection
import util
from psycopg2 import sql
from datetime import datetime


@connection.connection_handler
def get_five_questions_ordered(cursor, order_by='submission_time', order_direction='DESC'):
    cursor.execute(
        sql.SQL("""SELECT * FROM question
                   ORDER BY {order_by} {order_direction}
                   LIMIT 5;
                """).format(order_by=sql.Identifier(order_by),
                            order_direction=sql.SQL(order_direction))
    )
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_all_questions_ordered(cursor, order_by='submission_time', order_direction='DESC'):
    cursor.execute(
        sql.SQL("""SELECT * FROM question
                   ORDER BY {order_by} {order_direction};
                """).format(order_by=sql.Identifier(order_by),
                            order_direction=sql.SQL(order_direction))
    )
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def insert_new_question(cursor, item_data):
    submission_time = datetime.now()
    submission_time = datetime.strftime(submission_time, '%Y-%m-%d %H:%M:%S')
    view_number = 0
    vote_number = 0
    title = item_data['title']
    message = item_data['message']
    image = item_data['image']
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                   VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                    """,
                   {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number,
                    'title': title, 'message': message, 'image': image})


@connection.connection_handler
def get_question_id(cursor):
    cursor.execute("""
                    SELECT id FROM question
                    WHERE id = (SELECT max(id) FROM question);
                   """)
    max_id = cursor.fetchone()
    return max_id['id']


@connection.connection_handler
def get_question_with_given_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question = cursor.fetchone()
    return question


@connection.connection_handler
def update_view_number(cursor, question_id, number):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + %(number)s
                    WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id, 'number': number})


@connection.connection_handler
def get_answers(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def insert_new_answer(cursor, item_data):
    submission_time = datetime.now()
    submission_time = datetime.strftime(submission_time, '%Y-%m-%d %H:%M:%S')
    vote_number = 0
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
                   """,
                   {
                       'submission_time': submission_time, 'vote_number': vote_number,
                       'question_id': item_data['question_id'], 'message': item_data['message'],
                       'image': item_data['image']
                   })


@connection.connection_handler
def update_question_vote(cursor, question_id, number):
    cursor.execute("""
                   UPDATE question
                   SET vote_number = vote_number + %(number)s
                   WHERE id = %(question_id)s; 
                   """,
                   {'number': number, 'question_id': question_id})


@connection.connection_handler
def update_answer_vote(cursor, answer_id, number):
    cursor.execute("""
                   UPDATE answer
                   SET vote_number = vote_number + %(number)s
                   WHERE id = %(answer_id)s; 
                   """,
                   {'number': number, 'answer_id': answer_id})


@connection.connection_handler
def get_question_id_from_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s;
                   """,
                   {'answer_id': answer_id})
    question_id = cursor.fetchone()
    return question_id['question_id']


@connection.connection_handler
def get_image_path_answer(cursor, answer_id):
    cursor.execute("""SELECT image FROM answer
                      WHERE id = %(answer_id)s;
                   """,
                   {'answer_id': answer_id})
    path_for_image = cursor.fetchone()
    return path_for_image['image']


@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id =%(answer_id)s;
                   """,
                   {'answer_id': answer_id})
    path_for_image = get_image_path_answer(answer_id)
    image = "static/" + path_for_image
    os.remove(image)


#def delete_answer(id):
#    answers = connection.read_csv_file("sample_data/answer.csv", answer_headers)
#    for answer in answers:
#        if id == answer["id"]:
#            if answer["image"] != '':
#                image = "static/" + answer["image"]
#                os.remove(image)
#            answers.remove(answer)
#    connection.write_csv_file("sample_data/answer.csv", answers, answer_headers)

@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id =%(question_id)s;
                    """,
                   {'question_id': question_id})
    cursor.execute("""
                    DELETE FROM question
                    WHERE id =%(question_id)s;
                    """,
                   {'question_id': question_id})


@connection.connection_handler
def update_question(cursor, question_id, updated_data):
    cursor.execute("""
                    UPDATE question
                    SET title = %(title)s, message = %(message)s, image = %(image)s
                    WHERE id = %(question_id)s;
                   """,
                   {'title': updated_data['title'], 'message': updated_data['message'],
                    'image': updated_data['image'], 'question_id': question_id})





#    answers = connection.read_csv_file("sample_data/answer.csv", answer_headers)
#    questions = connection.read_csv_file("sample_data/question.csv", question_headers)
#    for question in questions:
#        if id == question["id"]:
#            if question["image"] != '':
#                image = "static/" + question["image"]
#                os.remove(image)
#            questions.remove(question)
#    for answer in answers:
#        if id == answer["question_id"]:
#            if answer["image"] != '':
#                image = "static/" + answer["image"]
#                os.remove(image)
#            answers.remove(answer)
#    connection.write_csv_file("sample_data/answer.csv", answers, answer_headers)
#    connection.write_csv_file("sample_data/question.csv", questions, question_headers)


