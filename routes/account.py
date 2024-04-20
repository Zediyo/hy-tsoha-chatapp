from app import app
from flask import redirect, render_template, request, session
import db.queries as q
from werkzeug.security import check_password_hash, generate_password_hash

def create_user_data(id, name):
	session["user"] = {
		"id" : id,
		"username" : name,
		"admin" : False,
	}

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

@app.route("/logout")
def logout():
	session.pop("user", None)
	return redirect("/")

@app.route("/deleteuseraccount", methods=["POST"])
def delete_user_account():
	user_id = int(request.form["user_id"])

	#not in session
	if not session["user"]:
		return redirect(request.referrer)
	
	#can only delete if personal account or as admin
	if session["user"]["id"] != user_id and not session["user"]["admin"]:
		return redirect(request.referrer)

	res = q.delete_user_account(user_id)

	#deleted account in session -> logout
	if res == True and session["user"]["id"] == user_id:
		return redirect("/logout")

	return redirect("/")