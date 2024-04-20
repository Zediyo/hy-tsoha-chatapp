from db.db import db
from sqlalchemy.sql import text

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

def get_messages_with(user_id, target_id):
	query = text("""
		SELECT
			id, sender_id, receiver_id, content,
			TO_CHAR(sent_at, 'HH24:MI') time,
			TO_CHAR(sent_at, 'DD.MM.YY') date,
			edit_at
		FROM
			messages
		WHERE
			deleted = false AND (
				(sender_id = :id1 AND receiver_id = :id2) OR (sender_id = :id2 AND receiver_id = :id1)
			)
		ORDER BY
			id ASC
		LIMIT 100
	""")
	result = db.session.execute(query, { "id1" : user_id, "id2" : target_id })
	return result.fetchall()

def check_new_messages(user_id, target_id, timestamp):
	query = text(""" SELECT EXISTS
		(SELECT
			1
		FROM
			messages
		WHERE (
			EXTRACT(EPOCH FROM sent_at) > :timestamp OR
			EXTRACT(EPOCH FROM edit_at) > :timestamp) AND (
				(sender_id = :id1 AND receiver_id = :id2) OR
			  	(sender_id = :id2 AND receiver_id = :id1)
			))
	""")
	result = db.session.execute(query, { "id1" : user_id, "id2" : target_id, "timestamp" : timestamp })
	return result.fetchone()[0]

def send_message(sender_id, receiver_id, content):
	try:
		query = text("INSERT INTO messages (sender_id, receiver_id, content) VALUES (:sender, :receiver, :content)")
		db.session.execute(query, { "sender" : sender_id, "receiver" : receiver_id, "content" : content })
		db.session.commit()
	except:
		return False

	return True

def edit_message(sender_id, msg_id, content):
	try:
		query = text("UPDATE messages SET content = :content, edit_at = NOW() AT TIME ZONE 'UTC' WHERE id = :msg_id AND sender_id = :sender_id")
		db.session.execute(query, { "msg_id" : msg_id, "sender_id" : sender_id, "content" : content })
		db.session.commit()
	except:
		return False

	return True

def delete_message(sender_id, msg_id):
	try:
		query = text("UPDATE messages SET deleted = true, edit_at = NOW() AT TIME ZONE 'UTC' WHERE id = :msg_id AND sender_id = :sender_id")
		db.session.execute(query, { "msg_id" : msg_id, "sender_id" : sender_id })
		db.session.commit()
	except:
		return False

	return True
