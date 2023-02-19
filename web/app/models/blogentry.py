from app import db
from sqlalchemy_serializer import SerializerMixin
# import datetime


# thailand_offset = datetime.timedelta(hours=7)

# thailand_datetime = datetime.datetime.now(datetime.timezone(thailand_offset))

# formatted_datetime = thailand_datetime.strftime("%m/%d/%Y, %I:%M:%S %p")



class BlogEntry(db.Model, SerializerMixin):
    __tablename__ = "blog_entries"



    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) 
    message = db.Column(db.String(280))
    email = db.Column(db.String(50))
    date_Created = db.Column(db.String(50))
    date_Update = db.Column(db.String(50))

    
    def __init__(self, name, message, email,date_Created,date_Update ):
        self.name = name
        self.message = message
        self.email = email
        self.date_Created = date_Created
        self.date_Update = date_Update


    def update(self, name, message, email, date_Created,date_Update):
        self.name = name
        self.message = message 
        self.email = email
        self.date_Created = date_Created
        self.date_Update = date_Update