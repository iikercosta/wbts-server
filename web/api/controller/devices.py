import flask
from flask import Blueprint, request

from web.api.service.devices_service import register_devs

devices = Blueprint('devices', __name__)


@devices.route('/register-devices', methods=['POST'])
def register_devices():

    data = request.get_json()

    if data:
        register_devs(data)
        return flask.Response(response='200')
    else:
        return flask.Response(response="400")





