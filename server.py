import os
from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import data_manager


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"


@app.route("/")
def route_index():
    questions = data_manager.convert_questions_data()
    return render_template("index.html", title="Home page", questions=questions)


@app.route('/form', methods=['GET', 'POST'])
def route_form():
    if request.method == 'POST':
        item_data = {"title": request.form["title"], "message": request.form["message"]}
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        item_data["image"] = "images/" + filename
        data_manager.add_new_question(item_data)
        return redirect('/')
    else:
        return render_template('form.html', title="Add a question")


@app.route('/question/<question_id>')
def route_question(question_id):
    questions = data_manager.convert_questions_data()
    answers = data_manager.convert_answers_data()
    related_answers = []
    for item in answers:
        if item['question_id'] == question_id:
            related_answers.append(item)

    render_template('question.html', questions=questions, answers=related_answers)


@app.route('/answer')
def route_answer():
    render_template('answer.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8000,
            debug=True,
            )
