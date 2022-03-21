from typing import List

import dateutil.parser as dp

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


def devices_query(data):
    from_timestamp = int(dp.parse(data["range"]["from"]).timestamp())
    to_timestamp = int(dp.parse(data["range"]["to"]).timestamp())

    interval_s = int(data["intervalMs"] / 1000)

    result = []

    for target in data["targets"]:

        print(target)

        if len(target["target"].split("+", 1)) == 1:
            dev_type = target["target"]
            location = None
        elif len(target["target"].split("+", 1)) == 2:
            dev_type, location = [a.strip() for a in target["target"].split("+", 1)]

        else:
            raise NotImplementedError()

        datapoints = get_data_points(dev_type, from_timestamp, to_timestamp, interval_s, location)

        if datapoints:
            info = {"target": target["target"], "datapoints": datapoints}
            result.append(info)

    return result


def get_data_points(dev, from_ts, to_ts, interval, location=None) -> List[List[int]]:
    timestamps = Timestamp.query.filter(Timestamp.timestamp > from_ts, Timestamp.timestamp < to_ts).all()

    timestamps.sort(key=lambda x: x.timestamp)

    ts_intervals = []

    while from_ts <= to_ts:
        ts_intervals.append(from_ts)
        from_ts += interval

    data_points = []
    current_ts_object = 0

    for index, _ in enumerate(ts_intervals):

        try:
            unique_devices = set()

            while ts_intervals[index] <= timestamps[current_ts_object].timestamp < ts_intervals[index + 1]:

                device = Device.query.filter_by(id=timestamps[current_ts_object].device_id).first()

                if device.dev_type == dev:
                    if location:
                        loc = Location.query.filter_by(id=device.location_id).first()
                        if loc.alias == location:
                            unique_devices.add(timestamps[current_ts_object].device_id)
                    else:
                        unique_devices.add(timestamps[current_ts_object].device_id)

                current_ts_object += 1

            data_points.append([ts_intervals[index], len(unique_devices)])

        except IndexError:
            break

    return data_points
