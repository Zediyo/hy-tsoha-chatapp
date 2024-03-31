from flask import Flask
from os import getenv
from csrf import csrf, CSRFError

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
csrf.init_app(app)

import routes