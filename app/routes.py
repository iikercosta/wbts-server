import flask
from flask import request

from app import app
from app.services import locations
from app.services.devices import register_devs, devices_query


@app.route("/", methods=['GET'])
def test():
    return flask.Response(response='200')


@app.route('/register-devices', methods=['POST'])
def register_devices():
    data = request.get_json()

    if data:
        register_devs(data)
        return flask.Response(response='200')

    return flask.Response(response="400")


@app.route('/search', methods=["POST"])
def search():
    dev_types = ["IP", "BLUETOOTH_LE", "BLUETOOTH_BR_EDR"]

    classes = ["IP", "BLUETOOTH_LE", "BLUETOOTH_BR_EDR"]

    for location in locations.get_locations():
        for dev_type in dev_types:
            classes.append(f"{dev_type} + {location}")

    return flask.jsonify(classes)


@app.route('/query', methods=["POST"])
def query():
    data_query = request.get_json()

    response_data = devices_query(data_query)

    return flask.jsonify(response_data)
