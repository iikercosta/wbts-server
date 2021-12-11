import time
from datetime import datetime, timedelta

from web import db
from web.api.model.models import Location, Device, Timestamp
from web.api.service.utils import get_master_timestamps, master_count, get_status_matrix


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


def get_devices_by_type(d_type: str) -> str:

    start_date: datetime = datetime(year=2021, month=12, day=11, hour=16, minute=0, second=0)
    stop_date: datetime = datetime.fromtimestamp(int(time.time()))
    delta: timedelta = timedelta(seconds=100)

    devices = Device.query.filter_by(dev_type=d_type).all()

    master_timestamps = get_master_timestamps(start_date, stop_date, delta)

    status_matrix = get_status_matrix(master_timestamps, devices)

    counters = master_count(master_timestamps, status_matrix)

    ret = 'date,value\n'

    start_date: datetime = datetime(year=2021, month=12, day=11, hour=0, minute=0, second=0)
    delta: timedelta = timedelta(days=1)

    for m in zip(master_timestamps, counters):
        ret += f'{start_date.strftime("%Y-%m-%d")},{m[1]}\n'
        start_date += delta

    return ret
