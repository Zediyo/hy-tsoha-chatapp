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

	return render_template("userlist.html", users=users, friend_requests=friend_requests, friends=friends)

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

	user = {"id" : id, "username" : username, "admin" : q.is_user_admin(id)}
	friends = q.get_friends(id)
	recents = q.get_recently_messaged_with(id)
	sent_requests = q.get_sent_friend_requests(id)
	received_requests = q.get_received_friend_requests(id)

	return render_template("profile.html", user=user, friends=friends,
		recents=recents, sent_requests=sent_requests, received_requests=received_requests)


@app.route("/friendrequest",methods=["POST"])
def friendrequest():
	if "user" not in session:
		return redirect("/")

	target_id = int(request.form["target_id"])

	if session["user"]["id"] == target_id:
		return redirect("/")
	
	if not q.get_username_from_id(target_id):
		return redirect("/")
	
	if q.is_friends_with(session["user"]["id"], target_id):
		return redirect("/")

	q.send_friend_request(session["user"]["id"], target_id)

	return redirect(request.referrer)

@app.route("/cancelrequest",methods=["POST"])
def cancelrequest():
	if "user" not in session:
		return redirect("/")

	sender_id = int(request.form["sender_id"])
	target_id = int(request.form["target_id"])

	if session["user"]["id"] != sender_id and session["user"]["id"] != target_id:
		return redirect("/")

	q.cancel_friend_request(sender_id, target_id)

	return redirect(request.referrer)

@app.route("/acceptrequest",methods=["POST"])
def acceptrequest():
	if "user" not in session:
		return redirect("/")

	user_id = int(request.form["user_id"])
	target_id = int(request.form["target_id"])

	if session["user"]["id"] != user_id:
		return redirect("/")
	
	q.accept_friend_request(user_id, target_id)

	return redirect(request.referrer)


@app.route("/deletefriend",methods=["POST"])
def deletefriend():
	if "user" not in session:
		return redirect("/")

	user_id = int(request.form["user_id"])
	target_id = int(request.form["target_id"])

	if session["user"]["id"] != user_id:
		return redirect("/")
	
	q.delete_friend(user_id, target_id)

	return redirect(request.referrer)

@app.route("/user/<int:id>/message/<int:other_id>")
def message_page(id, other_id):
	print("MSG", id, other_id)
	return render_template("message.html")