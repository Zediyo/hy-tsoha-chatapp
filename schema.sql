SET timezone = 'UTC';
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE admins (user_id INTEGER UNIQUE REFERENCES users(id), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE friend_requests( 
	sender_id INTEGER REFERENCES users(id),
    receiver_id INTEGER REFERENCES users(id),
	sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT request_pair UNIQUE (sender_id, receiver_id)
);
CREATE TABLE contact_pairs(
	user1_id INTEGER REFERENCES users(id),
	user2_id INTEGER REFERENCES users(id),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT contact_pair UNIQUE (user1_id, user2_id)
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users(id),
    receiver_id INTEGER REFERENCES users(id),
    content TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	edit_at TIMESTAMP DEFAULT NULL,
	deleted BOOLEAN DEFAULT false
);

INSERT INTO users (username, password) VALUES ('test_admin', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('test_user', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato01', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato02', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato03', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato04', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato05', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato06', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato07', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato08', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato09', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato10', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato11', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');
INSERT INTO users (username, password) VALUES ('potato12', 'scrypt:32768:8:1$3FcvJf4J1955oJ5K$df4055162adf8f83e5cc535246902bb57f701a9aabe30b3b1cd5670af28f282fc0777a5f3bb8cc3b20607b831b6f7ce4c367836b0709518e5c64701b9ad39c84');

INSERT INTO admins (user_id) VALUES (1);
INSERT INTO admins (user_id) VALUES (4);
INSERT INTO admins (user_id) VALUES (7);

INSERT INTO contact_pairs (user1_id, user2_id) VALUES (1, 2);
INSERT INTO contact_pairs (user1_id, user2_id) VALUES (3, 1);
INSERT INTO contact_pairs (user1_id, user2_id) VALUES (3, 2);

INSERT INTO friend_requests (sender_id, receiver_id) VALUES (1, 4);
INSERT INTO friend_requests (sender_id, receiver_id) VALUES (1, 5);
INSERT INTO friend_requests (sender_id, receiver_id) VALUES (1, 6);

INSERT INTO friend_requests (sender_id, receiver_id) VALUES (7, 1);
INSERT INTO friend_requests (sender_id, receiver_id) VALUES (8, 1);
INSERT INTO friend_requests (sender_id, receiver_id) VALUES (9, 1);

INSERT INTO messages (sender_id, receiver_id, content) VALUES (1, 2, 'potato');
INSERT INTO messages (sender_id, receiver_id, content) VALUES (2, 1, 'potato');
INSERT INTO messages (sender_id, receiver_id, content) VALUES (1, 2, 'peruna');
INSERT INTO messages (sender_id, receiver_id, content) VALUES (3, 1, 'potato potato potato potato potato potato potato');
INSERT INTO messages (sender_id, receiver_id, content) VALUES (1, 4, 'potato');
INSERT INTO messages (sender_id, receiver_id, content) VALUES (3, 4, 'potato');
INSERT INTO messages (sender_id, receiver_id, content) VALUES (4, 5, 'potato');