from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from routes.topics_data import topic_list
challenge = Blueprint("challenge", __name__)

@challenge.route("/challenge")
def challenge_subject():

    subjects = list(topic_list.keys())

    return render_template(
        "challenge_subject.html",
        subjects=subjects
    )
@challenge.route("/challenge_topics/<subject>")
def challenge_topics(subject):

    topics = topic_list.get(subject, [])

    return render_template(
        "challenge_topics.html",
        subject=subject,
        topics=topics
    )
@challenge.route("/start_challenge/<subject>/<topic>")
def start_challenge(subject, topic):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM challenge_questions WHERE topic=? ORDER BY RANDOM()",
        (topic,)
    )

    questions = cursor.fetchall()
    conn.close()

    return render_template(
        "challenge.html",
        questions=questions,
        subject=subject,
        topic=topic
    )
@challenge.route("/result", methods=["POST"])
def result():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    correct = 0
    wrong = 0

    for key in request.form:

        if key.startswith("q"):

            qid = key.replace("q", "")
            user_answer = request.form[key]

            cursor.execute(
                "SELECT answer FROM challenge_questions WHERE id=?",
                (qid,)
            )

            real_answer = cursor.fetchone()[0]

            if user_answer == real_answer:
                correct += 1
            else:
                wrong += 1

    conn.close()

    total = correct + wrong
    score = correct * 10

    return render_template(
        "challenge_result.html",
        correct=correct,
        wrong=wrong,
        total=total,
        score=score
    )