from db.db import db
from sqlalchemy.sql import text

def add_new_user(username, hash):
	try:
		query = text("INSERT INTO users (username, password) VALUES (:username, :password)")
		db.session.execute(query, {"username" : username, "password" : hash})
		db.session.commit()
	except:
		return False
	
	return True

def delete_user_account(user_id):
	ret = False
	try:
		with db.session.begin():
			result = db.session.execute(
				text("SELECT 1 FROM users WHERE id = :user_id"),
				{ "user_id" : user_id })
			exists = result.fetchone()

			if exists:
				ret = True
				db.session.execute(
					text("DELETE FROM friend_requests WHERE sender_id = :user_id OR receiver_id = :user_id"),
					{ "user_id" : user_id })
				
				db.session.execute(
					text("DELETE FROM admins WHERE user_id = :user_id"),
					{ "user_id" : user_id })
	
				db.session.execute(
					text("DELETE FROM contact_pairs WHERE user1_id = :user_id OR user2_id = :user_id"),
					{ "user_id" : user_id })
				
				db.session.execute(
					text("DELETE FROM messages WHERE sender_id = :user_id OR receiver_id = :user_id"),
					{ "user_id" : user_id })
				
				db.session.execute(
					text("DELETE FROM users WHERE id = :user_id"),
					{ "user_id" : user_id })
	except:
		ret = False
		db.session.rollback()

	db.session.commit()
	return ret