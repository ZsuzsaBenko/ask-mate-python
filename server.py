import os
from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import data_manager


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"


@app.route("/")
@app.route("/list")
def route_index():
    questions = data_manager.convert_questions_data()
    order_by = request.args.get("order_by")
    order_direction = request.args.get("order_direction")
    questions = data_manager.sort_questions(questions, order_by=order_by, order_direction=order_direction)
    return render_template("index.html", title="Home page", questions=questions)


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
        question_id = data_manager.add_new_question(item_data)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        return render_template('form.html', title="Add a question")


@app.route('/question/<question_id>')
def route_question(question_id):
    questions = data_manager.convert_questions_data()
    for item in questions:
        if item['id'] == int(question_id):
            item['view_number'] += 1
            chosen_question = item
            data_manager.change_question_data(questions)
    answers = data_manager.convert_answers_data()
    related_answers = []
    for item in answers:
        if item['question_id'] == int(question_id):
            related_answers.append(item)

    return render_template('question.html', chosen_question=chosen_question, answers=related_answers)


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
        data_manager.add_new_answer(item_data)
        return redirect(url_for("route_question", question_id=question_id))
    else:
        return render_template('form.html', title="Add an answer", question_id=question_id)


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
    questions = data_manager.convert_questions_data()
    for question in questions:
        if question["id"] == int(question_id):
            question["vote_number"] += 1
    data_manager.change_question_data(questions)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/vote-down")
def route_vote_down_question(question_id):
    questions = data_manager.convert_questions_data()
    for question in questions:
        if question["id"] == int(question_id):
            question["vote_number"] -= 1
    data_manager.change_question_data(questions)
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/answer/<answer_id>/vote-up')
def route_vote_up_answer(answer_id):
    answers = data_manager.convert_answers_data()
    for answer in answers:
        if answer["id"] == int(answer_id):
            answer["vote_number"] += 1
    data_manager.change_answer_data(answers)
    for answer in answers:
        if answer["id"] == int(answer_id):
            question_id = answer["question_id"]
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/answer/<answer_id>/vote-down')
def route_vote_down_answer(answer_id):
    answers = data_manager.convert_answers_data()
    for answer in answers:
        if answer["id"] == int(answer_id):
            answer["vote_number"] -= 1
    data_manager.change_answer_data(answers)
    for answer in answers:
        if answer["id"] == int(answer_id):
            question_id = answer["question_id"]
    return redirect(url_for("route_question", question_id=question_id))


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8000,
            debug=True,
            )
