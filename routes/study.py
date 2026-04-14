<<<<<<< HEAD
from flask import Blueprint, render_template, session
import sqlite3

study = Blueprint("study", __name__)

@study.route("/home")
def home():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT xp, level, streak FROM users WHERE id=?",
        (session["user_id"],)
    )

    user = cursor.fetchone()
    conn.close()

    return render_template(
        "home.html",
        xp=user[0],
        level=user[1],
        streak=user[2]
    )
@app.route("/update_study_time", methods=["POST"])
def update_study_time():

    if "user_id" not in session:
        return jsonify({"status":"no user"})

    data = request.get_json()
    minutes = data.get("minutes",0)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET study_minutes = study_minutes + ?
    WHERE id=?
    """,(minutes,session["user_id"]))

    conn.commit()
    conn.close()

=======
from flask import Blueprint, render_template, session
import sqlite3

study = Blueprint("study", __name__)

@study.route("/home")
def home():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT xp, level, streak FROM users WHERE id=?",
        (session["user_id"],)
    )

    user = cursor.fetchone()
    conn.close()

    return render_template(
        "home.html",
        xp=user[0],
        level=user[1],
        streak=user[2]
    )
@app.route("/update_study_time", methods=["POST"])
def update_study_time():

    if "user_id" not in session:
        return jsonify({"status":"no user"})

    data = request.get_json()
    minutes = data.get("minutes",0)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET study_minutes = study_minutes + ?
    WHERE id=?
    """,(minutes,session["user_id"]))

    conn.commit()
    conn.close()

>>>>>>> 4b72cdccd7641943b955334ed39ab7a7af142874
    return jsonify({"status":"updated"})