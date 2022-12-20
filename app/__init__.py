from flask import Flask
 
app = Flask(__name__, static_folder='static')
 
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'e773fc44127ba18a33ca7dcdfc69011c588cd2f22f8d080f'
 
from app import views  # noqa
