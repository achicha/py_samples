import os


class BaseConfig(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://docker:secret@172.18.0.3:5432/discover_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
