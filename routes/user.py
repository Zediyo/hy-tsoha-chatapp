from app import app
from flask import redirect, render_template, request, session
import db.queries as q

@app.route("/users")
def users():
	search = request.args.get("search")

	users = []
	
	if search and len(search) > 0:
		users = q.search_for_users(search)
	else:
		users = q.get_all_users()

	friend_requests = []
	friends = []

	if "user" in session:
		friend_requests = q.get_sent_friend_requests(session["user"]["id"])
		friend_requests = [item[0] for item in friend_requests]

		friends = q.get_friends(session["user"]["id"])
		friends = [item[0] for item in friends]

	return render_template("userlist.html", users=users, friend_requests=friend_requests, friends=friends)


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

	target_id = None
	try:
		target_id = int(request.form["target_id"])
	except:
		return redirect("/")

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
	
	sender_id = None
	target_id = None

	try:
		sender_id = int(request.form["sender_id"])
		target_id = int(request.form["target_id"])
	except:	
		return redirect("/")

	if session["user"]["id"] != sender_id and session["user"]["id"] != target_id:
		return redirect("/")

	q.cancel_friend_request(sender_id, target_id)

	return redirect(request.referrer)

@app.route("/acceptrequest",methods=["POST"])
def acceptrequest():
	if "user" not in session:
		return redirect("/")
	
	user_id = None
	target_id = None

	try:
		user_id = int(request.form["user_id"])
		target_id = int(request.form["target_id"])
	except:
		return redirect("/")

	if session["user"]["id"] != user_id:
		return redirect("/")
	
	q.accept_friend_request(user_id, target_id)

	return redirect(request.referrer)


@app.route("/deletefriend",methods=["POST"])
def deletefriend():
	if "user" not in session:
		return redirect("/")
	
	user_id = None
	target_id = None

	try:
		user_id = int(request.form["user_id"])
		target_id = int(request.form["target_id"])
	except:
		return redirect("/")

	if session["user"]["id"] != user_id:
		return redirect("/")
	
	q.delete_friend(user_id, target_id)

	return redirect(request.referrer)