import os
import pathlib


class Config:
    SECRET_KEY = '43962c69e826939f7460c17c86ba8b77d32bc123a7abb38a'
    basedir = pathlib.Path().resolve()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False