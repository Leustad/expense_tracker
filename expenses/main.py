import json

import datetime
from flask import render_template, redirect, url_for, request, Blueprint, jsonify
from flask_login import login_required, login_user, current_user, logout_user

from expenses import db, bcrypt, login_manager
from expenses.forms import ExpensesForm, LoginForm, RegisterForm
from expenses.models import Expenses, ExpensesSchema, User

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    dates = []
    form = ExpensesForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            for item in form.items.data:
                entry = Expenses(item['expense'],
                                 item['cost'],
                                 item['due_date'],
                                 item['desc'],
                                 )
                db.session.add(entry)
                db.session.commit()
        return redirect(url_for('main.index'))
    expenses = db.session.query(Expenses).all()
    for i in expenses:
        dates.append(i.due_date)
    dates = set(dates)

    output = []
    for i in expenses:
        output.append(i.__dict__)
    return render_template('index.html', form=form, expenses=output, dates=dates, name=current_user.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))

        return '<h1>Bad Creds</h1>'
    return render_template('login.html', form=form)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                        )
        print('new user: ', new_user.password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


@main_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
