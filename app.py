from flask import Flask, render_template, redirect, url_for
import sqlite3
import os

# Import blueprints
from routes.auth import auth
from routes.lectures import lectures
from routes.practice import practice
from routes.challenge import challenge
from routes.leaderboard import leaderboard
from routes.quiz import quiz
from routes.community import community
from routes.admin import admin
app = Flask(__name__)

app.secret_key = "secret123"

UPLOAD_FOLDER = "static/pdfs"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folders exist
if not os.path.isdir("static/pdfs"):
    os.makedirs("static/pdfs", exist_ok=True)
    os.makedirs("static/questions", exist_ok=True)
    os.makedirs("static/doubts", exist_ok=True)
# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(lectures)
app.register_blueprint(practice)
app.register_blueprint(challenge)
app.register_blueprint(leaderboard)
app.register_blueprint(quiz)
app.register_blueprint(community)
app.register_blueprint(admin)
# -------------------------
# Database Initialization
# -------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        score INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        study_minutes INTEGER DEFAULT 0,
        last_quiz_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lectures(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        topic TEXT,
        title TEXT,
        video_url TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lecture_progress(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        subject TEXT,
        topic TEXT,
        title TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        answer TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        topic TEXT,
        question_image TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        answer TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pdfs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        filename TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doubts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        question TEXT,
        image TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS challenge_questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        answer TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pyqs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year TEXT,
        question TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -------------------------
# General Routes
# -------------------------

@app.route("/")
def index():

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
        "Data Structure through Python",
        "Foundation of Engineering Math",
        "Fundamental of C Language",
        "Basics of Computer System",
        "Algorithms"
    ]

    return render_template("index.html", subjects=subjects)
@app.route("/home")
def home():
    return redirect(url_for("index"))


@app.route("/practice")
def practice_redirect():
    return redirect("/subjects")


@app.route("/materials")
def materials():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT title, filename FROM pdfs")
    files = cursor.fetchall()

    conn.close()

    return render_template("materials.html", files=files)


@app.route("/pyq")
def pyq():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT year, question FROM pyqs")
    questions = cursor.fetchall()

    conn.close()

    return render_template("pyq.html", questions=questions)

@app.route("/pdfs")
def pdfs():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT title, filename FROM pdfs")
    files = cursor.fetchall()

    conn.close()

    return render_template("pdfs.html", files=files)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)    