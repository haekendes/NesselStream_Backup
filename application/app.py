from flask import Flask
from flask_bootstrap import Bootstrap4
from config import Config
import RPi.GPIO as GPIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap4(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

from application import routes, models
