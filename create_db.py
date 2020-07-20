from expenses import db, config

# print('SQLALCHEMY_DATABASE_URI: {}'.format(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI))
db.create_all()
db.session.commit()
