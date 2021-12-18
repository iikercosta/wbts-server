import flask
from flask import Blueprint

views = Blueprint('views', __name__)


@views.route("/stats", methods=["GET"])
def show_stats():
    return flask.render_template("stats.html", device_type=flask.request.args['dev_type'], location=flask.request.args['location'])
