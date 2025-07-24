from flask import Flask, Blueprint, render_template, request, redirect, flash, session, Response
from werkzeug.security import check_password_hash
from db.db_conn import get_db_connection
import mysql.connector

login_bp = Blueprint("login", __name__, template_folder="templates")

@login_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "":
            flash(f"Invalid username or password!", "invalid")
            return redirect("/login")
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            user = cursor.fetchone()
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            conn.close()

        if user and check_password_hash(user["password"], password):
            session["username"] = username
            flash(f"Welcome {username} !", "success")
        else:
            flash(f"Invalid username or password!", "invalid")
    return render_template("login.html",
    title="Login")

@login_bp.route("/logout", methods=["GET"])
def logout():
    # session.clear()
    session.pop("username", None) #Remove username session
    return redirect("/login")


# We can also use the below method for routing
# login_bp.add_url_rule('/login', view_func=login)