from flask import Flask, render_template, redirect, request
from functions import DatabaseManager

APP = Flask(__name__)

DB = DatabaseManager('databases/urls.db')
DB.build()

@APP.route('/')
def root():
    return render_template("index.html")

@APP.route('/shorten', methods=["POST"])
def shorten_url():
    url = request.form.get('url')
    if url != None:
        return render_template("shorten.html", shortened_url=DB.shorten(url))
    else:
        return "Error: No url provided"

@APP.route('/l/<url>')
def redirect_to_site(url: str):
    return redirect(DB.get_url(url), code=200)

@APP.route('/clean')
def clean():
    DB.clean_database()


APP.run(host="0.0.0.0", port=8080)