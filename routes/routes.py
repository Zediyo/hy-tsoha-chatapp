from app import app
from flask import redirect, render_template

@app.route("/")
def index():
	return render_template("index.html")

@app.errorhandler(404)
def no_page(e):
    return redirect("/")