from app import app
from flask import flash, redirect, render_template, request, session
import queries as q
from werkzeug.security import check_password_hash, generate_password_hash

def create_user_data(id, name):
	session["user"] = {
		"id" : id,
		"username" : name,
		"admin" : False,
	}

@app.route("/")
def index():
	if "user" in session:
		print(session["user"])
	return render_template("index.html")

@app.errorhandler(404)
def no_page(e):
    return redirect("/")

@app.route("/users")
def users():
	users = q.get_all_users()

	friend_requests = []
	friends = []

	if "user" in session:
		friend_requests = q.get_sent_friend_requests(session["user"]["id"])
		friend_requests = [item[0] for item in friend_requests]

		friends = q.get_friends(session["user"]["id"])
		friends = [item[0] for item in friends]

		print("AAA", friend_requests, friends)

	return render_template("userlist.html", users=users, friend_requests=friend_requests, friends=friends)

@app.route("/create", methods=["POST"])
def create():
	# topic = request.form["topic"]
	# sql = text("INSERT INTO polls (topic, created_at) VALUES (:topic, NOW()) RETURNING id")
	# result = db.session.execute(sql, {"topic":topic})
	# poll_id = result.fetchone()[0]
	# choices = request.form.getlist("choice")
	# for choice in choices:
	#     if choice != "":
	#         sql = text("INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)")
	#         db.session.execute(sql, {"poll_id":poll_id, "choice":choice})
	# db.session.commit()
	return redirect("/")

@app.route("/poll/<int:id>")
def poll(id):
	# sql = text("SELECT topic FROM polls WHERE id=:id")
	# result = db.session.execute(sql, {"id":id})
	# topic = result.fetchone()[0]
	# sql = text("SELECT id, choice FROM choices WHERE poll_id=:id")
	# result = db.session.execute(sql, {"id":id})
	# choices = result.fetchall()
	return render_template("poll.html", id=id)

@app.route("/answer", methods=["POST"])
def answer():
	poll_id = request.form["id"]
	# if "answer" in request.form:
	#     choice_id = request.form["answer"]
	#     sql = text("INSERT INTO answers (choice_id, sent_at) VALUES (:choice_id, NOW())")
	#     db.session.execute(sql, {"choice_id":choice_id})
	#     db.session.commit()
	return redirect("/result/" + str(poll_id))

@app.route("/send", methods=["POST"])
def send():
	# content = request.form["content"]
	# sql = text("INSERT INTO messages (content) VALUES (:content)")
	# db.session.execute(sql, {"content":content})
	# db.session.commit()
	return redirect("/")

@app.route("/form")
def form():
	return render_template("form.html")

@app.route("/order")
def order():
	return render_template("order.html")

@app.route("/result/<int:id>")
def result(id):
	# sql = text("SELECT topic FROM polls WHERE id=:id")
	# result = db.session.execute(sql, {"id":id})
	# topic = result.fetchone()[0]
	# sql = text("SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN answers a " \
	#       "ON c.id=a.choice_id WHERE c.poll_id=:poll_id GROUP BY c.id")
	# result = db.session.execute(sql, {"poll_id":id})
	# choices = result.fetchall()
	return render_template("result.html")

@app.route("/login",methods=["GET", "POST"])
def login():
	if "user" in session:
		return redirect("/")

	if request.method == "GET":
		return render_template("login.html")
     
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		user = q.get_user(username)

		if not user:
			return render_template("login.html", errmsg="User does not exist.")
            
		if check_password_hash(user.password, password) == False:
			return render_template("login.html", errmsg="Invalid password.")
        
		create_user_data(user.id, username)

		if q.is_user_admin(user.id):
			session["user"]["admin"] = True

		return redirect("/user/" + str(session["user"]["id"]))

	return redirect("/")

@app.route("/register",methods=["GET", "POST"])
def register():
	if "user" in session:
		return redirect("/")

	if request.method == "GET":
		return render_template("register.html")
     
	if request.method == "POST":
		username = request.form["username"]
		password1 = request.form["password1"]
		password2 = request.form["password2"]

		if len(username) < 2 or len(username) > 32:
			return render_template("register.html", errmsg="Username has to be between 2 and 32 characters long.")

		if username.isalnum() == False:
			return render_template("register.html", errmsg="Username can only contain numbers or letters.")
		
		if len(password1) < 6 or len(password1) > 32:
			return render_template("register.html", errmsg="Password length has to be between 6 and 32.")
		
		if password1 != password2:
			return render_template("register.html", errmsg="Passwords do not match.")
		
		user = q.get_user(username)

		if user:
			return render_template("register.html", errmsg="Username is already taken.")

		hash = generate_password_hash(password1)

		if q.add_new_user(username, hash) == False:
			return render_template("register.html", errmsg="Unknown error.")

		user = q.get_user(username)
		create_user_data(user.id, username)

		return redirect("/user/" + str(session["user"]["id"]))

	return redirect("/")

@app.route("/logout")
def logout():
	session.pop("user", None)
	return redirect("/")

@app.route("/user/<int:id>")
def user_page(id):
	user = session.get("user", None)

	if not user:
		return render_template("profile.html", errmsg="No access.")

	if user["id"]!= id and user["admin"] == False:
		return render_template("profile.html", errmsg="No access.")

	username = q.get_username_from_id(id)

	if not username:
		return render_template("profile.html", errmsg="User does not exist.")

	user = {"id" : id, "username" : username}
	friends = q.get_friends(id)
	recents = q.get_recently_messaged_with(id)
	sent_requests = q.get_sent_friend_requests(id)
	received_requests = q.get_received_friend_requests(id)

	print(recents)

	return render_template("profile.html", user=user, friends=friends
		, recents=recents, sent_requests=sent_requests, received_requests=received_requests)


@app.route("/friendrequest",methods=["POST"])
def friendrequest():
	if "user" not in session:
		return redirect("/")

	target_id = request.form["target_id"]

	if session["user"]["id"] == target_id:
		return redirect("/")
	
	if not q.get_username_from_id(target_id):
		return redirect("/")
	
	if q.is_friends_with(session["user"]["id"], target_id):
		return redirect("/")

	q.send_friend_request(session["user"]["id"], target_id)

	return redirect(request.referrer)

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

