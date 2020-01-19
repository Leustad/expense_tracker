import os


class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PSW = os.environ['DB_PASS_DEV'] if os.environ.get('DB_PASS_DEV') else None
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ['EMAIL_USERNAME']
    MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']


class ProductionConfig(Config):
    ENV = 'production'
    db_url = os.environ['HEROKU_POSTGRESQL_GREEN_URL'] if os.environ.get('HEROKU_POSTGRESQL_GREEN_URL') else None
    SQLALCHEMY_DATABASE_URI = f'{db_url}'
    SCHEMA = 'snowy'
    MAIL_DEBUG = False
    MAIL_SUPPRESS_SEND = False


class DevelopmentConfig(Config):
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{Config.PSW}@192.168.1.2/expenses'
    SCHEMA = 'leustad'
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{Config.PSW}@main-pi/expenses'
    SCHEMA = 'snowy_test'
    MAIL_DEBUG = False
    MAIL_SUPPRESS_SEND = True
