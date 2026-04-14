from flask import Blueprint, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename
from routes.topics_data import topic_list

practice = Blueprint("practice", __name__)

@practice.route("/subjects")
def subjects():

    subjects = [
        "Probability and Statistics",
        "Database Management System",
        "Machine Learning",
        "Artificial Intelligence",
        "Linear Algebra",
        "Calculus and Optimization",
        "Warehousing",
        "Python for Data Science",
        "Verbal Aptitude",
        "General Aptitude",
        "Data Structure throuh python",
        "Foundation of Engineering Math",
        "Fundamental of C Language",
        "Basics of Computer System",
        "Algorithms"
    ]

    return render_template("subjects.html", subjects=subjects)


@practice.route("/practice_topics/<subject>")
def practice_topics(subject):

    topics = topic_list.get(subject, [])

    return render_template(
        "practice_topics.html",
        subject=subject,
        topics=topics
    )


@practice.route("/practice/<subject>/<topic>")
def practice_topic(subject, topic):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM practice WHERE subject=? AND topic=?",
        (subject, topic)
    )

    questions = cursor.fetchall()
    conn.close()

    return render_template(
        "practice.html",
        questions=questions,
        subject=subject,
        topic=topic
    )


@practice.route("/add_question", methods=["GET","POST"])
def add_question():
    if session.get("username") != "nanda":
        return "Access Denied"

    if request.method == "POST":

        subject = request.form["subject"]
        topic = request.form["topic"]
        file = request.files["question"]

        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]
        answer = request.form["answer"]

        filename = secure_filename(file.filename)
        path = os.path.join("static/questions", filename)

        file.save(path)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO practice
        (subject,topic,question_image,option1,option2,option3,option4,answer)
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (subject,topic,filename,option1,option2,option3,option4,answer))

        conn.commit()
        conn.close()

        return "Question Uploaded"

    return render_template("add_question.html")
@practice.route("/upload_questions", methods=["GET","POST"])
def upload_questions():

    if request.method == "POST":

        subject = request.form["subject"]
        file = request.files["file"]

        filename = secure_filename(file.filename)
        path = os.path.join("static/questions", filename)

        file.save(path)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO question_sources(subject,filename,type) VALUES(?,?,?)",
        (subject, filename, file.content_type)
        )

        conn.commit()
        conn.close()

        return "Uploaded successfully"

    return render_template("upload_questions.html")