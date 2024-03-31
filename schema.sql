CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE admins (user_id INTEGER UNIQUE REFERENCES users(id));
CREATE TABLE friend_requests( 
	sender_id INTEGER REFERENCES users(id),
    receiver_id INTEGER REFERENCES users(id),
	sent_at TIMESTAMP
);
CREATE TABLE contact_pairs(
	user1_id INTEGER REFERENCES users(id),
	user2_id INTEGER REFERENCES users(id),
	created_at TIMESTAMP
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users(id),
    receiver_id INTEGER REFERENCES users(id),
    content TEXT,
    sent_at TIMESTAMP,
	edit_at TIMESTAMP
);

INSERT INTO users (username, password) VALUES ('test_admin', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO admins (user_id) VALUES (1);
INSERT INTO users (username, password) VALUES ('test_user', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');