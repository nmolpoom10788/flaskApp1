from app import app, db
from flask.cli import FlaskGroup
from app.models.contact import Contact
from app.models.blogentry import BlogEntry
import datetime


thailand_offset = datetime.timedelta(hours=7)

thailand_datetime = datetime.datetime.now(datetime.timezone(thailand_offset))

formatted_datetime = thailand_datetime.strftime("%m/%d/%Y, %I:%M:%S %p")

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(
        Contact(firstname='สมชาย', lastname='ทรงแบด', phone='081-111-1111'))
    db.session.add(
        BlogEntry(name='chaiwitchit', message='lab 11 create in twitter', email='nmolpoom10788@gmail.com',date_Created=formatted_datetime,date_Update="asdsdasd"))
    #     BlogEntry(name='chaiwitchit', message='It is very difficult', email='nmolpoom10788@gmail.com'))
    # db.session.add(
    #     BlogEntry(name='chaiwitchit', message='hello world', email='nmolpoom10788@gmail.com'))
    db.session.commit()


if __name__ == "__main__":
    cli()
