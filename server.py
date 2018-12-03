from flask import Flask, render_template, redirect
import data_manager
import util


app = Flask(__name__)


@app.route("/")
def route_index():
    questions = data_manager.convert_questions_data()
    return render_template("index.html", title="Home page", questions=questions)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8000,
            debug=True,
            )
