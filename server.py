from flask import Flask, render_template, redirect
import data_manager
import util
import connection


app = Flask(__name__)


question_headers = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_headers = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


@app.route("/")
def route_index():
    return render_template("index.html", title="Home page")


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=8000,
            debug=True,
            )
