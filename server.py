import os
from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import data_manager


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"


@app.route("/")
def route_index():
    order_by = request.args.get("order_by")
    order_direction = request.args.get("order_direction")
    if order_by and order_direction:
        questions = data_manager.get_five_questions_ordered(order_by, order_direction)
    else:
        questions = data_manager.get_five_questions_ordered()
    return render_template("index.html", title="Home page", questions=questions)


@app.route("/list")
def route_all_questions():
    is_all = True
    order_by = request.args.get("order_by")
    order_direction = request.args.get("order_direction")
    if order_by and order_direction:
        questions = data_manager.get_all_questions_ordered(order_by, order_direction)
    else:
        questions = data_manager.get_all_questions_ordered()
    return render_template("index.html", title="All questions", questions=questions, is_all=is_all)


@app.route('/form', methods=['GET', 'POST'])
def route_form():
    if request.method == 'POST':
        item_data = {"title": request.form["title"], "message": request.form["message"]}
        f = request.files.get("file", None)
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item_data["image"] = "images/" + filename
        else:
            item_data["image"] = ""
        data_manager.insert_new_question(item_data)
        question_id = data_manager.get_question_id()
        return redirect(url_for("route_question", question_id=question_id))
    else:
        return render_template('form.html', title="Add a question")


@app.route('/question/<question_id>')
def route_question(question_id):
    data_manager.update_view_number(question_id, 1)
    chosen_question = data_manager.get_question_with_given_id(question_id)
    answers = data_manager.get_answers(question_id)
    return render_template('question.html', chosen_question=chosen_question, answers=answers,
                           title=chosen_question["title"])


@app.route('/question/<question_id>/new_answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        item_data = {"message": request.form["message"], "question_id": question_id}
        f = request.files.get("file", None)
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item_data["image"] = "images/" + filename
        else:
            item_data["image"] = ""
        data_manager.insert_new_answer(item_data)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        add_answer = True
        return render_template('form.html', title="Add an answer", question_id=question_id, add_answer=add_answer)


@app.route('/answer/<answer_id>/delete')
def route_delete_answer(answer_id):
    answers = data_manager.convert_answers_data()
    for answer in answers:
        if answer["id"] == int(answer_id):
            question_id = answer["question_id"]
    data_manager.delete_answer(answer_id)
    return redirect(url_for('route_question', question_id=question_id))


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id):
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
        questions = data_manager.convert_questions_data()
        for question in questions:
            if question["id"] == int(question_id):
                question["title"] = request.form["title"]
                question["message"] = request.form["message"]
                f = request.files.get("file", None)
                if f:
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    question["image"] = "images/" + filename
        data_manager.change_question_data(questions)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        questions = data_manager.convert_questions_data()
        for question in questions:
            if question["id"] == int(question_id):
                current = {"id": question["id"],
                           "submission_time": question["submission_time"],
                           "view_number": question["view_number"],
                           "vote_number": question["vote_number"],
                           "title": question["title"],
                           "message": question["message"],
                           "image": question["image"]}
        return render_template("form.html", title="Edit question", question_id=question_id, current=current)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8000,
            debug=True,
            )
