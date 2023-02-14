from app import db
from sqlalchemy_serializer import SerializerMixin


class Contact(db.Model, SerializerMixin):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    phone = db.Column(db.String(20))

    def __init__(self, firstname, lastname, phone):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone


    def update(self, firstname, lastname, phone):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone

class BlogEntry(db.Model, SerializerMixin):
    __tablename__ = "blog_entries"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    message = db.Column(db.String(280))
    email = db.Column(db.String(20))


    def __init__(self, name, message, email):
        self.name = name
        self.message = message
        self.email = email


    def update(self, name, message, email):
        self.name = name
        self.message = message
        self.email = email


    