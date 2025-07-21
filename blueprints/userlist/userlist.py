from flask import Flask, Blueprint, render_template, request, redirect, flash, session, Response
from db.db_conn import get_db_connection
import mysql.connector


userlist_bp = Blueprint("userlist", __name__, template_folder="templates")


@userlist_bp.route("/userlist", methods=["GET"])
def user_list():
    if request.method == "GET":
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user")
            users = cursor.fetchall()
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            conn.close()

    return render_template("userlist.html",
    title="User List",
    users=users)