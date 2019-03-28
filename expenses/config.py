import os

CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = '{}'.format(os.environ['DATABASE_URL'])
    SCHEMA = 'snowy'
    # SQLALCHEMY_BINDS = 'expenses_dev'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:{}@localhost/expenses'.format(os.environ['DB_PASS_DEV'])
    SCHEMA = 'leustad'


class TestingConfig(Config):
    TESTING = True
