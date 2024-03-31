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