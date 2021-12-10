from web import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(64))
    devices = db.relationship('Device')


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signature = db.Column(db.String(256))
    dev_type = db.Column(db.String(256))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    timestamps = db.relationship('Timestamp')


class Timestamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

