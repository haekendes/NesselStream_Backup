from application.app import db

class Temp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float)
    measure_datetime = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Temp {}>'.format(self.temp)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(64))
