import datetime

from flask import url_for, request, flash, render_template, Blueprint
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect

from expenses import bcrypt, db, login_manager
from expenses.forms import LoginForm
from expenses.helpers.helper import redirect_dest
from expenses.models import User

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            user.last_login = datetime.datetime.now()
            db.session.commit()
            return redirect_dest(fallback=url_for('main.index'))

        flash('Invalid/Wrong Credentials. Please try again.', category='warning')
    return render_template('login.html', form=form)


@login_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    flash(f'Goodbye {current_user.username}', 'primary')
    logout_user()
    return redirect(url_for('login.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def handle_needs_login():
    return redirect(url_for('login.login', next=request.endpoint))

