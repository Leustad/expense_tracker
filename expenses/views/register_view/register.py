from flask import request, flash, url_for, render_template, Blueprint
from werkzeug.utils import redirect

from expenses import bcrypt, db
from expenses.forms import RegisterForm
from expenses.models import User

register_blueprint = Blueprint('register', __name__)


@register_blueprint .route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                        )
        db.session.add(new_user)
        db.session.commit()
        flash('Please check your email for account activation link', 'info')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)
