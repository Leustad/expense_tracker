import os

CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PSW = os.environ['DB_PASS_DEV'] if os.environ.get('DB_PASS_DEV') else None

class ProductionConfig(Config):
    DEBUG = False
    db_url = os.environ['HEROKU_POSTGRESQL_GREEN_URL'] if os.environ.get('HEROKU_POSTGRESQL_GREEN_URL') else None
    SQLALCHEMY_DATABASE_URI = f'{db_url}'
    SCHEMA = 'snowy'
    # SQLALCHEMY_BINDS = 'expenses_dev'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{Config.PSW}@localhost/expenses'
    SCHEMA = 'leustad'


class TestingConfig(Config):
    TESTING = True
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{Config.PSW}@main-pi/expenses'
    SCHEMA = 'snowy_test'
