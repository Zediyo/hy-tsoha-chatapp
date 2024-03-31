# hy-tsoha chatapp

A simple chat app where users can message each other.

Features:
* Login, logout and create new user.
* List of all users and ability to search them.
* Users can add each other to their contacts and delete them from contacts.
* Users can message their contacts.
* Users can edit and delete their messages.
* Conversations are visible only for participants and admins.
* Users can delete their own account, admins can delete any account.


$ git clone https://github.com/user/tsoha-visitors.git
Cloning into 'tsoha-visitors'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), done.
$ cd tsoha-visitors/
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install flask
(venv) $ pip install flask-sqlalchemy
(venv) $ pip install psycopg2
(venv) $ pip install python-dotenv