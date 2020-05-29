from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template, redirect, request, abort, make_response
from functions import DatabaseManager
from gevent.pywsgi import WSGIServer

APP = Flask(__name__, template_folder="templates")

DB = DatabaseManager('databases/urls.db')
DB.build()
APP.config["SERVER_NAME"] = "localhost:8080"


@APP.route('/')
def root():
    response= make_response(render_template("index.html"))
    response.headers["Cache-Control"] = 'no-cache, no-store, must-revalidate'
    response.headers["Pragma"] = "no-cache"
    return response


@APP.route('/shorten', methods=["POST"])
def shorten_url():
    url = request.form.get('to_replace')
    if url is not None:
        return render_template("shorten.html", shortened_url=DB.shorten(url), root=APP.config.get('SERVER_NAME'))
    else:
        abort(400)


@APP.route('/<url>')
def redirect_to_site(url: str):
    return redirect(DB.get_url(url), code=200)


@APP.route('/clean')
def clean():
    DB.clean_database()


@APP.errorhandler(400)
def bad_request():
    return render_template("bad_request.html")


SERVER = WSGIServer(("0.0.0.0", 8080), APP)
SERVER.serve_forever()