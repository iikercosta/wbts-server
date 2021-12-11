import flask
from flask import Blueprint, request

from web.api.service.devices_service import register_devs, get_devices_by_type

devices = Blueprint('devices', __name__)


@devices.route('/register-devices', methods=['POST'])
def register_devices():
    data = request.get_json()

    if data:
        register_devs(data)
        return flask.Response(response='200')
    else:
        return flask.Response(response="400")


@devices.route('/get-devices', methods=['GET'])
def get_devices():

    dev_type = request.args.get('dev_type', type=str)

    data = get_devices_by_type(dev_type)

    return flask.Response(data, mimetype="text/csv", headers={"Content-disposition": "attachment;filename=data.csv"})
