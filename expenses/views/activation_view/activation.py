from flask import Blueprint, request, flash, url_for, render_template
from flask_login import login_required
from werkzeug.utils import redirect

from expenses import db
from expenses.forms import RequestActivationForm
from expenses.helpers.helper import send_activation_email
from expenses.models import User

activation_blueprint = Blueprint('activation', __name__)


@activation_blueprint.route('/request_activation', methods=['GET', 'POST'])
def request_activation():
    form = RequestActivationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.active:
            flash('Account Already Active. No Need to re-activate')
            return redirect(url_for('main.index'))
        send_activation_email(user)
        flash(f'Activation Email has been sent to {user.email}. Please don\'t forget to check your spam folder', 'info')
        return render_template('info.html',
                               title='Info',
                               msg='Account Activation has been Requested.'
                               )
    else:
        return render_template('request_activation.html', form=form, title='Request Activation')


@activation_blueprint.route('/request_activation/<token>', methods=['GET', 'POST'])
@login_required
def activate_account(token):
    user = User.verify_token(token, salt='email-activation-token')

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.request_activation'))
    else:
        user.active = True
        db.session.commit()
        flash('Your Account has been Activated !! You are now able to login.')
        return render_template('info.html',
                               title='Account Activated',
                               msg='Your Account has been activated'
                               )
