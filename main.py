from flask import Flask, Blueprint
from blueprints.login.login import login_bp
from blueprints.user.user import user_bp
from blueprints.userlist.userlist import userlist_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.register_blueprint(login_bp)
app.register_blueprint(user_bp)
app.register_blueprint(userlist_bp)
app.secret_key = 'required to setup session'
# app.register_blueprint(userlist_bp, url_prefix="/baseurl") http://localhost:5050/baseurl/

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["600/hour"], #Limit to 300 request per hour
    # application_limits = ["5/minute"] #Limit to 5 request per minute
)

def error_handler():
    return "Please do not flood the server."

limiter.limit("20/minute", error_message=error_handler)(login_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5050)