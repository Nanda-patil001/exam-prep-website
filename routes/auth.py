from flask import Blueprint, render_template, request, redirect, session, current_app
import sqlite3
import os
from werkzeug.utils import secure_filename

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]

            if len(user) > 6:
                session["level"] = user[6]
            else:
                session["level"] = 1

            return redirect("/home")

    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists. Try another username."

    return render_template("signup.html")


@auth.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


@auth.route("/upload_pdf", methods=["GET","POST"])
def upload_pdf():

    if "username" not in session or session["username"] != "nanda":
        return "Access Denied"

    if request.method == "POST":

        title = request.form["title"]
        file = request.files["pdf"]

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO pdfs(title, filename) VALUES(?,?)",
            (title, filename)
        )

        conn.commit()
        conn.close()

        return redirect("/pdfs")

    return render_template("upload_pdf.html")