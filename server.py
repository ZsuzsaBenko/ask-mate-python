import os
from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import data_manager


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "images"


@app.route("/")
def route_index():
    questions = data_manager.convert_questions_data()
    return render_template("index.html", title="Home page", questions=questions)


@app.route('/form', methods=['GET', 'POST'])
def route_form():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/')
    else:
        return render_template('form.html', title="Add a question")


@app.route('/question')
def route_question():
    render_template('question.html')


@app.route('/answer')
def route_answer():
    render_template('answer.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8000,
            debug=True,
            )
