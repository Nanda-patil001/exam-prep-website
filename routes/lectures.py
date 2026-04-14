from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from datetime import datetime
from routes.topics_data import topic_list
lectures = Blueprint("lectures", __name__)

@lectures.route("/lecture_subjects")
def lecture_subjects():

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

    return render_template(
        "lecture_subjects.html",
        subjects=subjects
    )
@lectures.route("/lectures/<subject>/<topic>")
def lecture_page(subject, topic):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, video_url FROM lectures WHERE subject=? AND topic=?",
        (subject, topic)
    )

    videos = cursor.fetchall()

    completed = []

    if "user_id" in session:
        user_id = session["user_id"]

        cursor.execute("""
        SELECT title FROM lecture_progress
        WHERE user_id=? AND subject=? AND topic=? AND completed=1
        """,(user_id,subject,topic))

        completed = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template(
        "lectures.html",
        subject=subject,
        topic=topic,
        videos=videos,
        completed=completed
    )


@lectures.route("/lecture_topics/<subject>")
def lecture_topics(subject):

    topics = topic_list.get(subject, [])

    return render_template(
        "lecture_topics.html",
        subject=subject,
        topics=topics
    )


@lectures.route("/complete_lecture", methods=["POST"])
def complete_lecture():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    subject = request.form["subject"]
    topic = request.form["topic"]
    title = request.form["title"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO lecture_progress(user_id,subject,topic,title,completed)
    VALUES(?,?,?,?,1)
    """,(user_id,subject,topic,title))

    cursor.execute("""
    UPDATE users
    SET last_lecture_subject=?, last_lecture_topic=?, last_lecture_title=?
    WHERE id=?
    """,(subject,topic,title,user_id))

    today = datetime.now().date()

    cursor.execute(
        "SELECT streak,last_quiz_date FROM users WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    streak = user[0]
    last_date = user[1]

    if last_date:
        last_date = datetime.strptime(last_date,"%Y-%m-%d").date()

    if last_date:
        if (today - last_date).days == 1:
            streak += 1
        elif (today - last_date).days > 1:
            streak = 1
    else:
        streak = 1

    cursor.execute("""
    UPDATE users
    SET streak=?, last_quiz_date=?
    WHERE id=?
    """,(streak,str(today),user_id))

    conn.commit()
    conn.close()

    return redirect(request.referrer)


@lectures.route("/add_lecture", methods=["GET","POST"])
def add_lecture():
    if session.get("username") != "nanda":
        return "Access Denied"

    if request.method == "POST":

        subject = request.form["subject"]
        topic = request.form["topic"]
        title = request.form["title"]
        url = request.form["url"]

        if "watch?v=" in url:
            video_id = url.split("watch?v=")[1]
            url = "https://www.youtube.com/embed/" + video_id

        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1]
            url = "https://www.youtube.com/embed/" + video_id

        elif "youtube.com/live/" in url:
            video_id = url.split("live/")[1]
            url = "https://www.youtube.com/embed/" + video_id

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO lectures(subject,topic,title,video_url) VALUES(?,?,?,?)",
            (subject, topic, title, url)
        )

        conn.commit()
        conn.close()

        return "Lecture Added"

    return render_template("add_lecture.html")


@lectures.route("/topics/<subject>")
def topics(subject):

    topics = topic_list.get(subject, [])

    return render_template("topics.html", subject=subject, topics=topics)