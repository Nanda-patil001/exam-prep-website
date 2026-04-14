from flask import Blueprint, render_template, session, redirect
import sqlite3

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def admin_dashboard():

    if session.get("username") != "nanda":
        return "Access Denied"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Count users
    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    # Count lectures
    cursor.execute("SELECT COUNT(*) FROM lectures")
    lectures = cursor.fetchone()[0]

    # Count practice questions
    cursor.execute("SELECT COUNT(*) FROM practice")
    questions = cursor.fetchone()[0]

    # Count challenge questions
    cursor.execute("SELECT COUNT(*) FROM challenge_questions")
    challenges = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        lectures=lectures,
        questions=questions,
        challenges=challenges
    )