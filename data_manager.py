# This module handles all the data received from the user.

import os
import connection
from psycopg2 import sql
from datetime import datetime


@connection.connection_handler
def get_five_questions_ordered(cursor, order_by='submission_time', order_direction='DESC'):
    cursor.execute(
        sql.SQL("""SELECT question.*, u.username AS "username" FROM question
                   INNER JOIN users u on question.user_id = u.id
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
        sql.SQL("""SELECT question.*, u.username AS "username" FROM question
                   INNER JOIN users u on question.user_id = u.id
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
    cursor.execute("""INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                   VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s,
                           %(user_id)s);
                    """,
                   {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number,
                    'title': item_data['title'], 'message': item_data['message'], 'image': item_data['image'],
                    'user_id': item_data['user_id']})


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
                    SELECT question.*, u.username AS "username" FROM question
                    INNER JOIN users u on question.user_id = u.id
                    WHERE question.id = %(question_id)s;
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
                    SELECT answer.*, u.username AS "username" FROM answer
                    LEFT JOIN users u on answer.user_id = u.id
                    WHERE question_id = %(question_id)s
                    ORDER BY accepted DESC, submission_time DESC;
                   """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def insert_new_answer(cursor, item_data):
    submission_time = datetime.now()
    submission_time = datetime.strftime(submission_time, '%Y-%m-%d %H:%M:%S')
    vote_number = 0
    accepted = False
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image, accepted, user_id)
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(accepted)s,
                    %(user_id)s);
                   """,
                   {
                       'submission_time': submission_time, 'vote_number': vote_number,
                       'question_id': item_data['question_id'], 'message': item_data['message'],
                       'image': item_data['image'], 'accepted': accepted, 'user_id': item_data['user_id']
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
def get_answers_id_from_question(cursor, question_id):
    cursor.execute("""
                    SELECT id FROM answer
                    WHERE question_id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    answer_id = cursor.fetchall()
    return answer_id


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
    try:
        path_for_image = get_image_path_answer(answer_id)
        image = "static/" + path_for_image
        os.remove(image)
    except:
        pass
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(answer_id)s;
                       """,
                   {'answer_id': answer_id})

    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;
                   """,
                   {'answer_id': answer_id})


@connection.connection_handler
def get_image_path_question(cursor, question_id):
    cursor.execute("""SELECT image FROM question
                      WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    path_for_image = cursor.fetchone()
    return path_for_image['image']


@connection.connection_handler
def delete_question(cursor, question_id):
    try:
        path_for_image = get_image_path_question(question_id)
        image = "static/" + path_for_image
        os.remove(image)
    except:
        pass
    cursor.execute("""
                    DELETE FROM comment
                    WHERE question_id = %(question_id)s;
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


@connection.connection_handler
def update_answer(cursor, answer_id, updated_data):
    cursor.execute("""
                    UPDATE answer
                    SET  message = %(message)s, image = %(image)s
                    WHERE id = %(answer_id)s;
                   """,
                   {'message': updated_data['message'],
                    'image': updated_data['image'], 'answer_id': answer_id})


@connection.connection_handler
def get_searched_phrases(cursor, phrase):
    cursor.execute("""
                    SELECT question.id, question.submission_time, question.title, question.message,
                        question.image FROM question
                    LEFT JOIN answer ON question.id = answer.question_id
                    WHERE question.title ILIKE %(phrase)s OR
                        question.message ILIKE %(phrase)s OR
                        answer.message ILIKE %(phrase)s
                    GROUP BY question.id, question.submission_time, question.title, question.message,
                        question.image;
                   """,
                   {'phrase': '%' + phrase + '%'})
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_question_comments(cursor, question_id):
    cursor.execute("""
                    SELECT comment.*, u.username AS username FROM comment
                    INNER JOIN users u on comment.user_id = u.id
                    WHERE question_id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    question_comments = cursor.fetchall()
    return question_comments


@connection.connection_handler
def get_answers_comments(cursor, question_id):
    cursor.execute("""
                    SELECT answer.id AS "answer_id", comment.message, comment.submission_time,
                    comment.edited_count, comment.id, comment.user_id, u.username AS "username" FROM comment
                    LEFT JOIN answer ON comment.answer_id = answer.id
                    INNER JOIN users u on comment.user_id = u.id;
                   """,
                   {'question_id': question_id})
    answer_comments = cursor.fetchall()
    return answer_comments


@connection.connection_handler
def insert_new_question_comment(cursor, item_data):
    submission_time = datetime.now()
    submission_time = datetime.strftime(submission_time, '%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, user_id)
                    VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(user_id)s); 
                    """,
                   {'question_id': item_data["question_id"], 'message': item_data["message"],
                    'submission_time': submission_time, 'user_id': item_data['user_id']})


@connection.connection_handler
def insert_new_answer_comment(cursor, item_data):
    submission_time = datetime.now()
    submission_time = datetime.strftime(submission_time, '%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO comment (answer_id, message, submission_time, user_id)
                    VALUES (%(answer_id)s, %(message)s, %(submission_time)s, %(user_id)s); 
                    """,
                   {'answer_id': item_data["answer_id"], 'message': item_data['message'],
                    'submission_time': submission_time, 'user_id': item_data['user_id']})


@connection.connection_handler
def get_comment_data(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id = %(comment_id)s;
                   """,
                   {'comment_id': comment_id})
    comment_data = cursor.fetchone()
    return comment_data


@connection.connection_handler
def get_question_id_from_question_comment(cursor, comment_id):
    cursor.execute("""
                    SELECT question_id FROM comment
                    WHERE id = %(comment_id)s;
                   """,
                   {'comment_id': comment_id})
    question_id = cursor.fetchone()
    return question_id['question_id']


@connection.connection_handler
def get_question_id_from_answer_comment(cursor, comment_id):
    cursor.execute("""
                    SELECT a.question_id FROM answer a
                    INNER JOIN comment c on a.id = c.answer_id
                    WHERE c.id = %(comment_id)s;
                   """,
                   {'comment_id': comment_id})
    question_id = cursor.fetchone()
    return question_id['question_id']


@connection.connection_handler
def update_comment(cursor, item_data):
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s, edited_count = COALESCE(edited_count, 0) + 1
                    WHERE id = %(comment_id)s;
                   """,
                   {'message': item_data['message'], 'comment_id': item_data['comment_id']})


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                   """,
                   {'comment_id': comment_id})


@connection.connection_handler
def insert_new_user(cursor, item_data):
    signup_date = datetime.now()
    signup_date = datetime.strftime(signup_date, '%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO users (username, password, signup_date, reputation)
                    VALUES (%(username)s, %(password)s, %(signup_date)s, %(reputation)s);
                    """,
                   {'username': item_data['username'], 'password': item_data['hashed_pass'],
                    'signup_date': signup_date, 'reputation': 0})


@connection.connection_handler
def get_user_data(cursor, username):
    cursor.execute("""
                    SELECT * FROM users
                    WHERE username = %(username)s;
                   """,
                   {'username': username})
    user_data = cursor.fetchone()
    return user_data


@connection.connection_handler
def insert_new_session(cursor, session):
    last_access = datetime.now()
    cursor.execute("""
                    INSERT INTO sessions (session_id, user_id, last_access)
                    VALUES ( %(session_id)s, %(user_id)s, %(last_access)s); 
                   """,
                   {'session_id': session['session_id'], 'user_id': session['user_id'], 'last_access': last_access})


@connection.connection_handler
def delete_session(cursor, session_id):
    cursor.execute("""
                    DELETE FROM sessions
                    WHERE session_id = %(session_id)s;
                   """,
                   {'session_id': session_id})


@connection.connection_handler
def get_users(cursor):
    cursor.execute("""
                    SELECT id, username, signup_date as "signup_date", reputation
                    FROM users
                    ORDER BY reputation DESC;
                    """)
    users_data = cursor.fetchall()
    return users_data


@connection.connection_handler
def get_counted_que(cursor, user_of_id):
    cursor.execute("""
                    SELECT COUNT(user_id) 
                    FROM question
                    WHERE user_id = %(user_of_id)s;
                    """,
                   {'user_of_id': user_of_id})
    users_data = cursor.fetchone()
    return users_data


@connection.connection_handler
def get_counted_ans(cursor, user_of_id):
    cursor.execute("""
                    SELECT COUNT(user_id) 
                    FROM answer
                    WHERE user_id = %(user_of_id)s;
                    """,
                   {'user_of_id': user_of_id})
    users_data = cursor.fetchone()
    return users_data


@connection.connection_handler
def get_counted_comm(cursor, user_of_id):
    cursor.execute("""
                    SELECT COUNT(user_id) 
                    FROM comment
                    WHERE user_id = %(user_of_id)s;
                    """,
                   {'user_of_id' : user_of_id})
    users_data = cursor.fetchone()
    return users_data


@connection.connection_handler
def make_answer_accepted(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET accepted = TRUE
                    WHERE id = %(answer_id)s;
                   """,
                   {'answer_id': answer_id})


@connection.connection_handler
def get_admin_id(cursor):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE username = 'admin';
                       """)
    admin_id = cursor.fetchone()
    return admin_id["id"]


@connection.connection_handler
def get_user_from_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT user_id FROM question
                    WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    user_id = cursor.fetchone()
    return user_id['user_id']


@connection.connection_handler
def get_user_id_from_answer_id(cursor, answer_id):
    cursor.execute("""
                      SELECT user_id FROM answer
                      WHERE id = %(answer_id)s;
                      """,
                   {'answer_id': answer_id})
    user_id = cursor.fetchone()
    return user_id['user_id']


@connection.connection_handler
def change_reputation(cursor, user_id, number):
    cursor.execute("""
                    UPDATE users
                    SET reputation = reputation + %(number)s
                    WHERE id = %(user_id)s;
                   """,
                   {'user_id': user_id, 'number': number})
