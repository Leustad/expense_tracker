import json

import datetime
from flask import render_template, redirect, url_for, request, Blueprint, jsonify, session
from flask_login import login_required, login_user, current_user, logout_user

from expenses import db, bcrypt, login_manager
from expenses.forms import ExpensesForm, LoginForm, RegisterForm, AddTemplateFrom, UpdateTemplateFrom
from expenses.models import Expense, User, Template

main_blueprint = Blueprint('main', __name__)


def get_user_id():
    return User.query.filter_by(id=session['user_id']).first().id


@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    dates = []
    form = ExpensesForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            for item in form.items.data:
                entry = Expense(item['expense'],
                                item['cost'],
                                item['due_date'],
                                item['desc'],
                                get_user_id()
                                )
                db.session.add(entry)
                db.session.commit()
        return redirect(url_for('main.index'))
    expenses = db.session.query(Expense).all()
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


def ready_update_template_form(update_template_form, update_fields):
    def _templates():
        return Template.query.filter_by(user_id=session['user_id']).all()

    update_template_form.name.choices = [(i.name, i.name) for i in _templates()]

    if update_fields:
        template_list = [i.template for i in _templates() if i.name == _templates()[0].name]
        template_list = ', '.join(map(str, template_list))
        update_template_form.fields.data = template_list


def get_forms(update_fields):
    add_template_form = AddTemplateFrom(request.form, prefix='add_template_')
    update_template_form = UpdateTemplateFrom(request.form, prefix='update_template_')
    ready_update_template_form(update_template_form, update_fields)
    return add_template_form, update_template_form


@main_blueprint.route('/template', methods=['GET'])
@login_required
def template():
    add_template_form, update_template_form = get_forms(update_fields=True)
    return render_template('template.html',
                           add_template_form=add_template_form,
                           update_template_form=update_template_form)


@main_blueprint.route('/add_template', methods=['POST'])
@login_required
def add_template():
    # logout_user()
    add_template_form, update_template_form = get_forms(update_fields=True)
    if request.method == 'POST' and add_template_form.validate_on_submit():
        template_name = Template.query.filter_by(id=session['user_id'],
                                                 name=add_template_form.name.data
                                                 ).first()
        if not template_name:
            ''' If a new template'''

            if add_template_form.default.data:
                deselect_default()

            new_template = Template(add_template_form.name.data,
                                    add_template_form.fields.data,
                                    True if add_template_form.default.data else False,
                                    get_user_id()
                                    )
            db.session.add(new_template)
            db.session.commit()
    return render_template('template.html',
                           add_template_form=add_template_form,
                           update_template_form=update_template_form)


@main_blueprint.route('/update_template', methods=['POST'])
@login_required
def update_template():
    add_template_form, update_template_form = get_forms(update_fields=False)

    if request.method == 'POST' and update_template_form.validate_on_submit():
        if update_template_form.default.data:
            deselect_default()

        template_row = Template.query.filter_by(user_id=session['user_id'],
                                                name=update_template_form.name.data).first()

        template_row.name = update_template_form.name.data
        template_row.template = str(update_template_form.fields.data)
        template_row.default = update_template_form.default.data

        # db.session.add(template_row)
        db.session.commit()
    for fieldName, errorMessages in update_template_form.errors.items():
        for err in errorMessages:
            print(err)
    return render_template('template.html',
                           add_template_form=add_template_form,
                           update_template_form=update_template_form)


def deselect_default():
    """ User wants this template to be default, so find the one is already "default" and
        make it NOT default """
    try:
        template_row = Template.query.filter_by(user_id=session['user_id'],
                                                default=True).first()
        template_row.default = False
        db.session.commit()
    except Exception as e:
        print(e)
