from app import db
from app.models import Location, Device, Timestamp


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
