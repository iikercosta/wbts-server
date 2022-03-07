import flask
from flask import request

from app import app
from app.services.devices import register_devs


@app.route('/register-devices', methods=['POST'])
def register_devices():
    data = request.get_json()

    if data:
        register_devs(data)
        return flask.Response(response='200')
    else:
        return flask.Response(response="400")
