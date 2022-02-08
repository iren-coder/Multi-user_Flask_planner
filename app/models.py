from sqlalchemy import *
from app import db


class Event(db.Model):
    __tablename__ = 'event'
    _id = Column(Integer, primary_key=True)
    author = db.Column(db.String(100), db.ForeignKey('user.email'))
    start = Column(db.Date, unique=False, nullable=False)
    end = Column(db.Date, unique=False, nullable=False)
    subject = Column(db.String(80), unique=False, nullable=False)
    description = Column(db.String(300), unique=False, nullable=True)


class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True
  
    def is_anonymous(self):
        return False