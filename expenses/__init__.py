import os

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print('__APP_SETTINGS__: {}'.format(os.environ['APP_SETTINGS']))

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'views.main_view.main.login'

from expenses.views.activation_view.activation import activation_blueprint
from expenses.views.history_view.history import history_blueprint
from expenses.views.template_view.template import template_blueprint
from expenses.views.login_view.login import login_blueprint
from expenses.views.main_view.main import main_blueprint
from expenses.views.register_view.register import register_blueprint
from expenses.views.reset_password_view.reset_password import reset_password_blueprint

app.register_blueprint(activation_blueprint)
app.register_blueprint(history_blueprint)
app.register_blueprint(template_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(reset_password_blueprint)


@app.errorhandler(404)
def not_found(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def not_found(error):
    return render_template('error/500.html'), 500
