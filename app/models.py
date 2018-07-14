from datetime import datetime
from app import db

class Model:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

class Sensor(db.Model, Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    readings = db.relationship('Reading', backref='publisher', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Sensor {}>'.format(self.name)

class Reading(db.Model, Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

class Category(db.Model, Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    units = db.Column(db.String(16), unique=True)
    readings = db.relationship('Reading', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)