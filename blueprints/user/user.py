from flask import Blueprint, render_template, request, flash, redirect, session
from db.db_conn import get_db_connection
from werkzeug.security import generate_password_hash
import mysql.connector

user_bp = Blueprint("user", __name__, template_folder="templates")

@user_bp.route("/add_user", methods=["POST","GET"])
def add_user():
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        status = request.form["status"]

        hashed_pw = generate_password_hash(password)

        if not username or not password:
            flash(f"Do not empty username and password!")
            return redirect("/add_user")

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO user (`username`,`password`,`firstname`,`lastname`,`status`) \
            VALUES (%s,%s,%s,%s,%s);", (username,hashed_pw,firstname,lastname,status,))
            conn.commit()
            flash(f"Successfully inserted!")
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            conn.close()

    return render_template("user.html", 
    title="Add User", 
    action="/add_user",
    users=[])

@user_bp.route("/get_user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if not session.get("username"):
        return redirect("/login")
    if request.method == "GET":
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,)) #Important need the comma ( , )
            users = cursor.fetchone()
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            conn.close()

    return render_template("user.html", 
    title="Update User", 
    action="/update_user",
    users=users
    )

@user_bp.route("/update_user", methods=["POST"])
def update_user():
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        user_id = request.form["user_id"]
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        status = request.form["status"]

        hashed_pw = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
            "UPDATE user SET username = %s, password = %s, firstname = %s, \
            lastname = %s, status = %s WHERE id = %s", (username, hashed_pw, firstname, lastname, 
            status, user_id,))
            conn.commit()
            flash(f"Successfully updated!")
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            conn.close()
        return render_template("user.html", 
            title="Update User", 
            action="/update_user",
            users=[])

@user_bp.route("/delete_user/<int:user_id>", methods=["GET"])
def delete_user(user_id):
    if not session.get("username"):
        return redirect("/login")
    if request.method == "GET":
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM user WHERE id = %s", (user_id,))
            conn.commit()
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            conn.close()
        return redirect("/userlist")

