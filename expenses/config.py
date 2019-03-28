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
    SQLALCHEMY_DATABASE_URI = '{}'.format(os.environ['HEROKU_POSTGRESQL_GREEN_URL'])
    SCHEMA = 'snowy'
    # SQLALCHEMY_BINDS = 'expenses_dev'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    psw = os.environ['DB_PASS_DEV'] if os.environ['DB_PASS_DEV'] else None
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:{}@localhost/expenses'.format(psw)
    SCHEMA = 'leustad'


class TestingConfig(Config):
    TESTING = True
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:{}@main-pi/expenses'.format(os.environ['DB_PASS_TEST'])
    SCHEMA = 'snowy_test'
