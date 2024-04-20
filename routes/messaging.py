from app import app
from flask import abort, jsonify, redirect, render_template, request, session
import db.queries as q

@app.route("/user/<int:id>/message/<int:other_id>")
def message_page(id, other_id):
	ses_id = session["user"]["id"]

	if ses_id != id and session["user"]["admin"] == False:
		return render_template("message.html", errmsg="No access.")

	target_username = q.get_username_from_id(other_id)

	if not target_username:
		target_username = "Unknown User"

	## ses_id so admins viewing other chats cant msg them.
	can_msg = q.is_friends_with(ses_id, other_id)

	last_check = q.get_last_message_timestamp(id, other_id)
	messages = q.get_messages_with(id, other_id)

	return render_template("message.html",
		can_msg=can_msg,
		target_username=target_username,
		messages=messages,
		user_id=id,
		other_id=other_id,
		last_check=last_check
	)

@app.route("/checknewmessages")
def check_new_messages():
	user_id = request.args.get("user_id")
	target_id = request.args.get("target_id")
	timestamp = request.args.get("timestamp")

	#missing args
	if not user_id or not target_id or not timestamp:
		return abort(403)

	if not session["user"]:
		return abort(403)
	
	if int(user_id) != session["user"]["id"] and session["user"]["admin"] == False:
		return abort(403)
	
	ret = q.check_new_messages(user_id, target_id, timestamp)

	if ret:
		return jsonify({"result" : True})
	
	return jsonify({"result" : False})


@app.route("/sendmessage", methods=["POST"])
def send_message():
	sender_id = int(request.form["sender_id"])

	#sender not in session
	if not session["user"] or session["user"]["id"] != sender_id:
		return redirect(request.referrer)

	content = request.form["message"]

	#invalid message length
	if len(content) == 0 or len(content) > 255:
		return redirect(request.referrer)
	
	target_id = request.form["target_id"]

	if not q.is_friends_with(sender_id, target_id):
		return redirect(request.referrer)


	q.send_message(sender_id, target_id, content)

	return redirect(request.referrer)

@app.route("/editmessage", methods=["POST"])
def edit_message():
	msg_id = request.form["msg_id"]
	sender_id = int(request.form["sender_id"])

	#original sender not in session
	if not session["user"] or session["user"]["id"] != sender_id:
		return redirect(request.referrer)

	new_content = request.form["content" + str(msg_id)]

	#invalid message length
	if len(new_content) == 0 or len(new_content) > 255:
		return redirect(request.referrer)

	q.edit_message(sender_id, msg_id, new_content)

	return redirect(request.referrer)

@app.route("/deletemessage", methods=["POST"])
def delete_message():
	msg_id = request.form["msg_id"]
	sender_id = int(request.form["sender_id"])

	#original sender not in session
	if not session["user"] or session["user"]["id"] != sender_id:
		return redirect(request.referrer)

	q.delete_message(sender_id, msg_id)

	return redirect(request.referrer)