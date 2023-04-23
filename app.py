from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = "your_secret_key"


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def handle_login():
    form_data = request.form
    username = form_data["username"]
    password = form_data["password"]
    if user_is_auth(username, password):
        session["username"] = username
        return redirect(url_for("welcome_page"))
    else:
        return redirect(url_for("home"))


def user_is_auth(username, password):
    # Query the database for a user with the given username and password
    stmt = text(
        "SELECT * FROM Person WHERE username = :username AND password = :password LIMIT 1;"
    )
    result = db.session.execute(stmt, {"username": username, "password": password})
    row = result.fetchone()
    return row is not None and len(row) > 0


@app.route("/welcome")
def welcome_page():
    if "username" in session:
        return render_template("welcome.html", username=session["username"])


# @app.route("/login", methods=["POST"])
# def login():
#     username = request.json["username"]
#     password = request.json["password"]

#     user = Person.query.filter_by(username=username).first()

#     if user:
#         if user.password == password:
#             return jsonify({"message": "Login successful!"})
#         else:
#             return jsonify({"message": "Invalid password!"})
#     else:
#         return jsonify({"message": "User not found!"})


app.run(debug=True)
