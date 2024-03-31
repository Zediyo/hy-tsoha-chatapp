from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = text("SELECT id, topic, created_at FROM polls ORDER BY id DESC")
    result = db.session.execute(sql)
    polls = result.fetchall()
    return render_template("index.html", polls=polls)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    sql = text("INSERT INTO polls (topic, created_at) VALUES (:topic, NOW()) RETURNING id")
    result = db.session.execute(sql, {"topic":topic})
    poll_id = result.fetchone()[0]
    choices = request.form.getlist("choice")
    for choice in choices:
        if choice != "":
            sql = text("INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)")
            db.session.execute(sql, {"poll_id":poll_id, "choice":choice})
    db.session.commit()
    return redirect("/")

@app.route("/poll/<int:id>")
def poll(id):
    sql = text("SELECT topic FROM polls WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = text("SELECT id, choice FROM choices WHERE poll_id=:id")
    result = db.session.execute(sql, {"id":id})
    choices = result.fetchall()
    return render_template("poll.html", id=id, topic=topic, choices=choices)

@app.route("/answer", methods=["POST"])
def answer():
    poll_id = request.form["id"]
    if "answer" in request.form:
        choice_id = request.form["answer"]
        sql = text("INSERT INTO answers (choice_id, sent_at) VALUES (:choice_id, NOW())")
        db.session.execute(sql, {"choice_id":choice_id})
        db.session.commit()
    return redirect("/result/" + str(poll_id))

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = text("INSERT INTO messages (content) VALUES (:content)")
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/result/<int:id>")
def result(id):
    sql = text("SELECT topic FROM polls WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = text("SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN answers a " \
          "ON c.id=a.choice_id WHERE c.poll_id=:poll_id GROUP BY c.id")
    result = db.session.execute(sql, {"poll_id":id})
    choices = result.fetchall()
    return render_template("result.html", topic=topic, choices=choices)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

# @app.route("/result")
# def result():
#     query = request.args["query"]
#     sql = "SELECT id, content FROM messages WHERE content LIKE :query"
#     result = db.session.execute(sql, {"query":"%"+query+"%"})
#     messages = result.fetchall()
#     return render_template("result.html", messages=messages)

# hash_value = generate_password_hash(password)
# sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
# db.session.execute(sql, {"username":username, "password":hash_value})
# db.session.commit()

# sql = "SELECT id, password FROM users WHERE username=:username"
# result = db.session.execute(sql, {"username":username})
# user = result.fetchone()    
# if not user:
#     # TODO: invalid username
# else:
#     hash_value = user.password
#     if check_password_hash(hash_value, password):
#         # TODO: correct username and password
#     else:
#         # TODO: invalid password