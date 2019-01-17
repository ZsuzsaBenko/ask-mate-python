import os
from flask import Flask, render_template, redirect, request, url_for, session
from werkzeug.utils import secure_filename
import bcrypt
import data_manager
import hashing


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"
app.secret_key = os.urandom(16)


@app.route("/")
def route_index():
    order_by = request.args.get("order_by")
    order_direction = request.args.get("order_direction")
    search_phrase = request.args.get("search")
    if order_by and order_direction:
        questions = data_manager.get_five_questions_ordered(order_by, order_direction)
    elif search_phrase:
        questions = data_manager.get_searched_phrases(search_phrase)
    else:
        questions = data_manager.get_five_questions_ordered()

    if 'session_id' in session:
        status = "logged_in"
    else:
        status = "sign_up"
    return render_template("index.html", title="Home page", questions=questions, status=status)


@app.route("/sign-up", methods=['GET', 'POST'])
def route_sign_up():
    status = "sign_up"
    if request.method == 'POST':
        pass_to_hash = request.form['password']
        hashed_pass = hashing.hash_password(pass_to_hash)
        username = request.form["username"]
        item_data = {"username": username, "hashed_pass": hashed_pass}
        user_data = data_manager.get_user_data(username)
        if not user_data:
            data_manager.insert_new_user(item_data)
            return redirect(url_for('route_login'))
        else:
            message = True
            return render_template("login-form.html", status=status, message=message)
    else:
        return render_template("login-form.html", status=status)


@app.route("/login", methods=['GET', 'POST'])
def route_login():
    status = "login"
    if request.method == 'POST':
        username = request.form['username']
        user_data = data_manager.get_user_data(username)
        if user_data:
            password = request.form['password']
            hashed_password = user_data['password']
            if hashing.verify_password(password, hashed_password):
                session['session_id'] = bcrypt.gensalt().decode('UTF-8')
                session['user_id'] = user_data['id']
                data_manager.insert_new_session(session)
                return redirect(url_for('route_index'))
            else:
                message = True
                return render_template("login-form.html", status=status, message=message)
        else:
            message = True
            return render_template("login-form.html", status=status, message=message)
    return render_template("login-form.html", status=status)


@app.route("/logout")
def route_logout():
    data_manager.delete_session(session['session_id'])
    session.pop('session_id')
    session.pop('user_id')
    return redirect(url_for('route_index'))


@app.route("/list")
def route_all_questions():
    is_all = True
    order_by = request.args.get("order_by")
    order_direction = request.args.get("order_direction")
    if order_by and order_direction:
        questions = data_manager.get_all_questions_ordered(order_by, order_direction)
    else:
        questions = data_manager.get_all_questions_ordered()
    if 'session_id' in session:
        status = "logged_in"
    else:
        status = "sign_up"
    return render_template("index.html", title="Home page", questions=questions, status=status, is_all=is_all)


@app.route('/form', methods=['GET', 'POST'])
def route_new_question():
    if request.method == 'POST':
        item_data = {"title": request.form["title"], "message": request.form["message"], "user_id": session["user_id"]}
        f = request.files.get("file", None)
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item_data["image"] = "images/" + filename
        else:
            item_data["image"] = None
        data_manager.insert_new_question(item_data)
        question_id = data_manager.get_question_id()
        return redirect(url_for("route_question", question_id=question_id))
    else:
        return render_template('form-question.html', title="Add a question")


@app.route('/question/<question_id>')
def route_question(question_id):
    data_manager.update_view_number(question_id, 1)
    chosen_question = data_manager.get_question_with_given_id(question_id)
    question_comments = data_manager.get_question_comments(question_id)
    answers = data_manager.get_answers(question_id)
    answer_comments = data_manager.get_answers_comments(question_id)
    admin_id = data_manager.get_admin_id()
    if "session_id" in session:
        status = "logged_in"
    else:
        status = "sign_up"
    return render_template('question.html', chosen_question=chosen_question, answers=answers,
                           title=chosen_question["title"], question_comments=question_comments,
                           answer_comments=answer_comments, status=status, admin_id=admin_id)


@app.route('/question/<question_id>/new_answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        item_data = {"message": request.form["message"], "question_id": question_id, "user_id": session["user_id"]}
        f = request.files.get("file", None)
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item_data["image"] = "images/" + filename
        else:
            item_data["image"] = None
        data_manager.insert_new_answer(item_data)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        return render_template('form-answer.html', title="Add an answer", question_id=question_id)


@app.route('/answer/<answer_id>/delete')
def route_delete_answer(answer_id):
    question_id = data_manager.get_question_id_from_answer(answer_id)
    data_manager.delete_answer(answer_id)
    return redirect(url_for('route_question', question_id=question_id))


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id):
    answer_id = data_manager.get_answers_id_from_question(question_id)
    try:
        for _list in answer_id:
            for value in _list.values():
                data_manager.delete_answer(value)
    except:
        pass
    data_manager.delete_question(question_id)
    return redirect(url_for('route_index'))


@app.route("/question/<question_id>/vote-up")
def route_vote_up_question(question_id):
    data_manager.update_question_vote(question_id, 1)
    data_manager.update_view_number(question_id, -1)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/vote-down")
def route_vote_down_question(question_id):
    data_manager.update_question_vote(question_id, -1)
    data_manager.update_view_number(question_id, -1)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/answer/<answer_id>/vote-up")
def route_vote_up_answer(answer_id):
    data_manager.update_answer_vote(answer_id, 1)
    question_id = data_manager.get_question_id_from_answer(answer_id)
    data_manager.update_view_number(question_id, -1)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/answer/<answer_id>/vote-down")
def route_vote_down_answer(answer_id):
    data_manager.update_answer_vote(answer_id, -1)
    question_id = data_manager.get_question_id_from_answer(answer_id)
    data_manager.update_view_number(question_id, -1)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def route_edit_question(question_id):
    if request.method == "POST":
        updated_data = {'title': request.form["title"], 'message': request.form["message"]}
        f = request.files.get("file", None)
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            updated_data["image"] = "images/" + filename
        else:
            image_path = data_manager.get_image_path_question(question_id)
            updated_data["image"] = image_path
        data_manager.update_question(question_id, updated_data)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        question = data_manager.get_question_with_given_id(question_id)
        current = {"title": question["title"],
                   "message": question["message"],
                   "image": question["image"]}
        return render_template("form-question.html", title="Edit question", question_id=question_id, current=current)


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def route_edit_answer(answer_id):
    question_id = data_manager.get_question_id_from_answer(answer_id)
    if request.method == "POST":
        updated_data = {'message': request.form["message"]}
        f = request.files.get("file", None)
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            updated_data["image"] = "images/" + filename
        else:
            image_path = data_manager.get_image_path_answer(answer_id)
            updated_data["image"] = image_path
        data_manager.update_answer(answer_id, updated_data)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        question = data_manager.get_answers(question_id)
        question = question[0]
        current_answer = {"message": question["message"],
                          "image": question["image"]}
        return render_template("form-answer.html", title="Edit Answer", answer_id=answer_id, current_answer=current_answer)


@app.route("/question/<question_id>/new_comment", methods=["GET", "POST"])
def route_new_question_comment(question_id):
    if request.method == 'POST':
        item_data = {"message": request.form["message"], "question_id": question_id, 'user_id': session['user_id']}
        data_manager.insert_new_question_comment(item_data)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        question_comment = True
        return render_template('form-comment.html', title="Add a comment", question_id=question_id,
                               question_comment=question_comment)


@app.route("/answer/<answer_id>/new_comment", methods=["GET", "POST"])
def route_new_answer_comment(answer_id):
    question_id = data_manager.get_question_id_from_answer(answer_id)
    if request.method == 'POST':
        item_data = {"message": request.form["message"], "answer_id": answer_id, "user_id": session["user_id"]}
        data_manager.insert_new_answer_comment(item_data)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        answer_comment = True
        return render_template('form-comment.html', title="Add a comment", question_id=question_id,
                               answer_comment=answer_comment, answer_id=answer_id)


@app.route("/question-comment/<comment_id>/edit", methods=["GET", "POST"])
def route_edit_question_comment(comment_id):
    comment_data = data_manager.get_comment_data(comment_id)
    if request.method == "POST":
        item_data = {"message": request.form["message"], "comment_id": comment_id}
        data_manager.update_comment(item_data)
        question_id = comment_data["question_id"]
        return redirect(url_for("route_question", question_id=question_id))
    else:
        current_comment = True
        question_comment = True
        return render_template("form-comment.html", title="Edit a comment", comment_id=comment_id,
                               current_comment=current_comment, comment_data=comment_data,
                               question_comment=question_comment)


@app.route("/answer-comment/<comment_id>/edit", methods=["GET", "POST"])
def route_edit_answer_comment(comment_id):
    comment_data = data_manager.get_comment_data(comment_id)
    if request.method == "POST":
        item_data = {"message": request.form["message"], "comment_id": comment_id}
        data_manager.update_comment(item_data)
        question_id = data_manager.get_question_id_from_answer_comment(comment_id)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        current_comment = True
        return render_template("form-comment.html", title="Edit a comment", comment_id=comment_id,
                               current_comment=current_comment, comment_data=comment_data)


@app.route('/question-comment/<comment_id>/delete')
def route_delete_question_comment(comment_id):
    question_id = data_manager.get_question_id_from_question_comment(comment_id)
    data_manager.delete_comment(comment_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/answer-comment/<comment_id>/delete')
def route_delete_answer_comment(comment_id):
    question_id = data_manager.get_question_id_from_answer_comment(comment_id)
    data_manager.delete_comment(comment_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/user")
def route_all_user():
    user_info = data_manager.get_users()
    for user in user_info:
        counted_question = data_manager.get_counted_que(user['id'])
        counted_answer = data_manager.get_counted_ans(user['id'])
        counted_comment = data_manager.get_counted_comm(user['id'])
        user.update({'counted_question':counted_question['count']})
        user.update({'counted_answer':counted_answer['count']})
        user.update({'counted_comment':counted_comment['count']})
    return render_template('user.html', user_info=user_info)


@app.route('/answer/<answer_id>/accept')
def route_accept_answer(answer_id):
    question_id = data_manager.get_question_id_from_answer(answer_id)
    data_manager.make_answer_accepted(answer_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/user/<user_id>')
def route_userpage(user_id):
    user_profile = data_manager.get_userprofile(user_id)
    user_questions = data_manager.get_users_questions(user_id)
    user_answers = data_manager.get_users_answer(user_id)
    question_comments = data_manager.get_users_question_comment(user_id)
    answer_comments = data_manager.get_users_answer_comment(user_id)
    return render_template("user.html", user_profile=user_profile,
                            user_questions=user_questions, user_answers=user_answers,
                           question_comments=question_comments, answer_comments=answer_comments)

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8000,
            debug=True,
            )
