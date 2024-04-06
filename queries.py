from db import db
from sqlalchemy.sql import text

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
	query = text("""
			  	SELECT a.id, b.username FROM
					(SELECT receiver_id as id FROM friend_requests WHERE sender_id=:id) a 
				LEFT JOIN users b ON a.id = b.id
		""")
	result = db.session.execute(query, {"id" : id})
	return result.fetchall()

def get_received_friend_requests(id):
	query = text("""
			  	SELECT a.id, b.username FROM
					(SELECT sender_id as id FROM friend_requests WHERE receiver_id=:id) a 
				LEFT JOIN users b ON a.id = b.id
		""")
	result = db.session.execute(query, {"id" : id})
	return result.fetchall()

def get_friends(id):
	query = text("""
			SELECT a.id, b.username FROM 
				(SELECT user1_id as id FROM contact_pairs WHERE user2_id=:id 
				UNION 
				SELECT user2_id as id FROM contact_pairs WHERE user1_id=:id) a
			LEFT JOIN users b ON a.id = b.id
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

def get_recently_messaged_with(id):
	query = text("""
			SELECT
				other_id,
				b.username as other_name,
				sender_name,
				date,
				content
			FROM (
				SELECT
					CASE WHEN sender_id = :id THEN receiver_id ELSE sender_id END AS other_id,
					sender_id,
					b.username as sender_name,
					TO_CHAR(sent_at, 'HH24:MI DD/MM/YY') AS date,
					content,
					ROW_NUMBER() OVER(PARTITION BY LEAST(sender_id, receiver_id), GREATEST(sender_id, receiver_id) ORDER BY a.id DESC) rn
				FROM messages a
				LEFT JOIN users b ON a.sender_id = b.id
			  	WHERE sender_id = :id OR receiver_id = :id
			) a
			LEFT JOIN users b ON a.other_id = b.id
			WHERE rn = 1
			LIMIT 10;
		""")
	result = db.session.execute(query, {"id" : id})
	return result.fetchall()

def cancel_friend_request(id1, id2):
	query = text("DELETE FROM friend_requests WHERE sender_id = :id1 AND receiver_id = :id2")
	db.session.execute(query, {"id1" : id1, "id2" : id2})
	db.session.commit()

def accept_friend_request(user_id, target_id):
	try:
		with db.session.begin():
			result = db.session.execute(
				text("SELECT 1 FROM friend_requests WHERE sender_id = :tid AND receiver_id = :uid"),
				{ "uid" : user_id, "tid" : target_id })
			exists = result.fetchone()

			if exists:
				db.session.execute(
					text("DELETE FROM friend_requests WHERE sender_id = :tid AND receiver_id = :uid"),
					{ "uid" : user_id, "tid" : target_id })
				db.session.execute(
					text("INSERT INTO contact_pairs (user1_id, user2_id) VALUES (:tid, :uid);"),
					{ "uid" : user_id, "tid" : target_id })
	except:
		db.session.rollback()

	db.session.commit()

def delete_friend(user_id, target_id):
	query = text("DELETE FROM contact_pairs WHERE (user1_id = :id1 AND user2_id = :id2) OR (user1_id = :id2 AND user2_id = :id1)")
	db.session.execute(query, {"id1" : user_id, "id2" : target_id})
	db.session.commit()