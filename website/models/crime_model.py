from models.database import db

class CrimeData(db.Model):

    __tablename__ = "crime_data"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    year = db.Column(db.Integer)

    month = db.Column(db.Integer)

    day = db.Column(db.Integer)

    hour = db.Column(db.Integer)

    minute = db.Column(db.Integer)

    neighbourhood = db.Column(
        db.String(255)
    )

    crime_type = db.Column(
        db.String(255)
    )

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)