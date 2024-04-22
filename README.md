# hy-tsoha chatapp

A simple chat app where users can message each other.

Features:
* Login, logout and create new user.
* List of all users and ability to search them.
* Users can add each other to their contacts and delete them from contacts.
* Users can message their contacts.
* Users can edit and delete their messages.
* Conversations are visible only for participants and admins.
* Users can delete their own account, admins can delete any non-admin account.

# how to test on local machine

1. clone
2. create .env in root folder and fill it with the following.

    `DATABASE_URL=<postgres_db_url>`

    `SECRET_KEY=<random_key>`

3. open cmd/terminal in the folder and input the following.

    `python -m venv venv`

    `source venv/bin/activate`

    `pip install -r requirements.txt`

    ~~`psql < schema.sql`~~

    `flask run`

   login with: `test_admin - password` or `test_user - password`

# todo

* cleanup?
