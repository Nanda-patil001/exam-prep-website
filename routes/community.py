from flask import Blueprint, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename

community = Blueprint("community", __name__)


@community.route("/ask_doubt", methods=["GET","POST"])
def ask_doubt():

    if request.method == "POST":

        question = request.form["question"]
        file = request.files["image"]

        filename = secure_filename(file.filename)
        path = os.path.join("static/doubts", filename)

        file.save(path)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO doubts(username,question,image) VALUES(?,?,?)",
        (session["username"], question, filename)
        )

        conn.commit()
        conn.close()

        return redirect("/doubts")

    return render_template("ask_doubt.html")


@community.route("/doubts")
def doubts():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM doubts")
    doubts = cursor.fetchall()

    conn.close()

    return render_template("doubts.html", doubts=doubts)


@community.route("/add_pyq", methods=["GET","POST"])
def add_pyq():
    if session.get("username") != "nanda":
        return "Access Denied"

    if "username" not in session or session["username"] != "nanda":
        return "Access Denied"

    if request.method == "POST":

        year = request.form["year"]
        question = request.form["question"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO pyqs(year, question) VALUES(?, ?)",
            (year, question)
        )

        conn.commit()
        conn.close()

        return redirect("/pyq")

    return render_template("add_pyq.html")