<<<<<<< HEAD
from flask import Blueprint, render_template, session, redirect
import sqlite3

leaderboard = Blueprint("leaderboard", __name__)

@leaderboard.route("/leaderboard")
def leaderboard_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, xp, level, streak
    FROM users
    ORDER BY xp DESC
    """)

    users = cursor.fetchall()

    user_id = session["user_id"]
    rank = None

    for i, u in enumerate(users, start=1):
        if u[0] == user_id:
            rank = i
            break

    conn.close()

    return render_template(
        "leaderboard.html",
        users=users,
        your_rank=rank
=======
from flask import Blueprint, render_template, session, redirect
import sqlite3

leaderboard = Blueprint("leaderboard", __name__)

@leaderboard.route("/leaderboard")
def leaderboard_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, xp, level, streak
    FROM users
    ORDER BY xp DESC
    """)

    users = cursor.fetchall()

    user_id = session["user_id"]
    rank = None

    for i, u in enumerate(users, start=1):
        if u[0] == user_id:
            rank = i
            break

    conn.close()

    return render_template(
        "leaderboard.html",
        users=users,
        your_rank=rank
>>>>>>> 4b72cdccd7641943b955334ed39ab7a7af142874
    )