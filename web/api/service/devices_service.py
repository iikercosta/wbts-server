import time
from datetime import datetime, timedelta
from typing import List

from web import db
from web.api.model.models import Location, Device, Timestamp
from web.api.service.utils import get_master_timestamps, get_concurrence


def register_devs(devs):
    location = Location.query.filter_by(alias=devs['location']).first()

    if not location:
        new_location = Location(alias=devs['location'])
        db.session.add(new_location)
        db.session.commit()

    l_id = Location.query.filter_by(alias=devs['location']).first().id

    for d in devs['devices']:
        device = Device.query.filter_by(signature=d['signature'], location_id=l_id).first()

        if not device:
            new_device = Device(signature=d['signature'], dev_type=d['dev_type'], location_id=l_id)
            db.session.add(new_device)
            db.session.commit()
            device = Device.query.filter_by(signature=d['signature'], location_id=l_id).first()

        for t in d['timestamps']:
            new_timestamp = Timestamp(timestamp=t, device_id=device.id)
            db.session.add(new_timestamp)
            db.session.commit()


def get_devices_concurrence(start: datetime, stop: datetime, delta: timedelta, location: str, d_type: str) -> str:

    loc_id = Location.query.filter_by(alias=location).first().id
    devices = Device.query.filter_by(dev_type=d_type, location_id=loc_id).all()

    master_timestamps = get_master_timestamps(start, stop, delta)

    concurrency = get_concurrence(master_timestamps, devices)

    ret = 'date,value\n'

    for m in zip(master_timestamps, concurrency):
        ret += f'{m[0]},{m[1]}\n'

    return ret

