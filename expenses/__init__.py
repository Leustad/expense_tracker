import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print('__APP_SETTINGS__: {}'.format(os.environ['APP_SETTINGS']))

# bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# from pigeon.models import User, MessageBoard
# from pigeon.admin.view import AdminView, AdminMessageBoard

# admin = Admin(app, name='Dashboard', index_view=AdminView(User, db.session, url='/admin', endpoint='admin'))
# admin.add_view(ModelView(User, db.session))
# admin.add_view(AdminMessageBoard(MessageBoard, db.session, url='/admin/messageboard/'))

from expenses.main import main_blueprint
# from pigeon.admin.view import my_admin_blueprint
app.register_blueprint(main_blueprint)
# app.register_blueprint(my_admin_blueprint)

# from expenses.apis import api