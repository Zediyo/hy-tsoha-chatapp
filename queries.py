from db import db
from sqlalchemy.sql import text

def add_visit():
	db.session.execute("INSERT INTO visitors (time) VALUES (NOW())")
	db.session.commit()

def get_counter():
	result = db.session.execute("SELECT COUNT(*) FROM visitors")
	counter = result.fetchone()[0]
	return counter

def get_user(username):
	query = text("SELECT id, password FROM users WHERE username=:username")
	result = db.session.execute(query, {"username" : username})
	return result.fetchone()

def get_username_from_id(id):
	query = text("SELECT username FROM users WHERE id=:id")
	result = db.session.execute(query, {"id" : id})
	r = result.fetchone()
	return None if not r else r[0]

def is_user_admin(id):
	query = text("SELECT 1 FROM admins WHERE user_id=:user_id")
	result = db.session.execute(query, {"user_id" : id})
	return result.fetchone() != None

def add_new_user(username, hash):
	try:
		query = text("INSERT INTO users (username, password) VALUES (:username, :password)")
		db.session.execute(query, {"username" : username, "password" : hash})
		db.session.commit()
	except:
		return False
	
	return True

def get_all_users():
	query = text("""
			  SELECT id, username, b.user_id st, TO_CHAR(created_at, 'DD-MM-YYYY') date FROM users a
			  LEFT JOIN (SELECT user_id FROM admins) b ON a.id = b.user_id
			  ORDER BY id
		""")
	result = db.session.execute(query)
	return result.fetchall()

def send_friend_request(id1, id2):
	try:
		query = text("INSERT INTO friend_requests (sender_id, receiver_id) VALUES (:id1, :id2)")
		db.session.execute(query, {"id1" : id1, "id2" : id2})
		db.session.commit()
	except:
		return False

	return True

def get_sent_friend_requests(id):
	query = text("SELECT receiver_id FROM friend_requests WHERE sender_id=:id")
	result = db.session.execute(query, {"id" : id})
	return result.fetchall()

def get_friends(id):
	query = text("""
			SELECT user1_id FROM contact_pairs WHERE user2_id=:id 
			UNION 
			SELECT user2_id FROM contact_pairs WHERE user1_id=:id 
		""")
	result = db.session.execute(query, {"id" : id})
	return result.fetchall()

def is_friends_with(id1, id2):
	query = text("""
			SELECT 1 FROM contact_pairs WHERE user1_id=:id1 AND user2_id=:id2 
			UNION 
			SELECT 1 FROM contact_pairs WHERE user1_id=:id2 AND user2_id=:id1 
		""")
	result = db.session.execute(query, {"id1" : id1, "id2" : id2})
	return result.fetchone() != None