from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from datetime import datetime

quiz = Blueprint("quiz", __name__)
@quiz.route("/quiz")
def quiz_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quiz ORDER BY RANDOM() LIMIT 15")
    questions = cursor.fetchall()

    conn.close()

    return render_template("quiz.html", questions=questions)


@quiz.route("/submit_quiz", methods=["POST"])
def submit_quiz():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, answer FROM quiz")
    quiz_answers = cursor.fetchall()

    total_score = 0

    for qid, correct_answer in quiz_answers:

        user_answer = request.form.get(f"q{qid}")

        if user_answer == correct_answer:
            total_score += 10

    today = datetime.now().date()

    cursor.execute(
        "SELECT streak,last_quiz_date,xp,study_minutes FROM users WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    streak = user[0]
    last_date = user[1]
    current_xp = user[2]
    study_minutes = user[3]

    study_minutes += 10

    xp_gain = 100
    old_level = (current_xp // 500) + 1

    new_xp = current_xp + xp_gain
    level = (new_xp // 500) + 1

    level_up = level > old_level

    if last_date:
        last_date = datetime.strptime(last_date,"%Y-%m-%d").date()

    if study_minutes >= 60:

        if last_date:
            if (today - last_date).days == 1:
                streak += 1
            elif (today - last_date).days > 1:
                streak = max(0, streak - 1)
        else:
            streak = 1

        study_minutes = 0
        last_date = today

    cursor.execute(
        """
        UPDATE users
        SET streak=?, xp=?, level=?, study_minutes=?, last_quiz_date=?
        WHERE id=?
        """,
        (streak, new_xp, level, study_minutes, str(last_date), user_id)
    )

    session["level"] = level

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        score=total_score,
        streak=streak,
        xp=xp_gain,
        level=level,
        level_up=level_up

    )