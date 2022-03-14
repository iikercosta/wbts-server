import flask
from flask import request

from app import app
from app.services import locations
from app.services.devices import register_devs


@app.route("/", methods=['GET'])
def test():
    return flask.Response(response='200')


@app.route('/register-devices', methods=['POST'])
def register_devices():
    data = request.get_json()

    if data:
        register_devs(data)
        return flask.Response(response='200')
    else:
        return flask.Response(response="400")


@app.route('/search')
def search():

    dev_types = ["IP", "BLUETOOTH LE", "BLUETOOTH BR/EDR"]

    classes = []

    for location in locations.get_locations():
        for dev_type in dev_types:
            classes.append(f"{location} {dev_type}")


    return flask.jsonify()


@app.route('/query')
def query():
    pass

if __name__ == '__main__':
    dev_types = ["IP", "BLUETOOTH LE", "BLUETOOTH BR/EDR"]
    locations = ["BILBAO", "DONONSTI", "GASTEIZ"]

    classes = []

    for location in locations:
        for dev_type in dev_types:
            classes.append(f"{location} + {dev_type}")


    print(classes)