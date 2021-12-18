from typing import List

from web import db


class Timestamp(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    timestamp: int = db.Column(db.Integer)
    device_id: int = db.Column(db.Integer, db.ForeignKey('device.id'))


class Device(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    signature: str = db.Column(db.String(256))
    dev_type: str = db.Column(db.String(256))
    location_id: int = db.Column(db.Integer, db.ForeignKey('location.id'))
    timestamps: List[Timestamp] = db.relationship('Timestamp')


class Location(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    alias: str = db.Column(db.String(64))
    devices: List[Device] = db.relationship('Device')







