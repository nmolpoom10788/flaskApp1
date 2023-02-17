from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

class BlogEntry(db.Model, SerializerMixin):
    __tablename__ = "blog_entries"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) 
    message = db.Column(db.String(280))
    email = db.Column(db.String(50))
    date_Created = db.Column(db.DateTime())
    date_Update = db.Column(db.DateTime())

    
    def __init__(self, name, message, email):
        self.name = name
        self.message = message
        self.email = email
        self.date_Created = datetime.now()
        self.date_Update = datetime.now()


    def update(self, name, message, email):
        self.name = name
        self.message = message 
        self.email = email
        self.date_Created = datetime.now()
        self.date_Update = datetime.now()