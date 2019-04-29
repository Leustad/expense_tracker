from flask import Blueprint, url_for, request, flash, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from expenses import bcrypt, db
from expenses.forms import RequestResetFrom, ResetPasswordFrom
from expenses.helpers.helper import send_reset_email
from expenses.models import User

reset_password_blueprint = Blueprint('reset_password', __name__)


@reset_password_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetFrom(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@reset_password_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_token(token, salt='password-reset-token')

    if user is None:
        flash('That is an invalid or expired token', 'danger')
        return redirect(url_for('reset_password.reset_request'))
    form = ResetPasswordFrom()
    if form.validate_on_submit():
        hashed_psw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_psw
        db.session.commit()
        flash('Your password has been updated !! You are now able to login with your new password.', 'success')
        return redirect(url_for('login.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
