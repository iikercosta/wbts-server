from datetime import datetime, timedelta

import flask
from flask import Blueprint, request

from web.api.service.devices_service import register_devs, get_devices_concurrence

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
    location = request.args.get('location', type=str)

    start = datetime(year=2021, month=12, day=13, hour=0, minute=0, second=0)
    stop = datetime(year=2021, month=12, day=14, hour=0, minute=0, second=0)
    delta = timedelta(seconds=120)

    data = get_devices_concurrence(start, stop, delta, location, dev_type)

    return flask.Response(data, mimetype="text/csv", headers={"Content-disposition": "attachment;filename=data.csv"})
