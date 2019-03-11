import datetime
import json

from flask import render_template, redirect, url_for, request, Blueprint, jsonify, session
from flask_login import login_required, login_user, current_user, logout_user

from expenses.helpers import helper
from expenses import db, bcrypt, login_manager
from expenses.forms import ExpensesForm, LoginForm, RegisterForm, AddTemplateFrom, UpdateTemplateFrom
from expenses.models import Expense, User, Template

main_blueprint = Blueprint('main', __name__)


def get_user_id():
    return User.query.filter_by(id=session['user_id']).first().id


@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    template_names = []
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
    yty_data = {}
    db_yty_data = helper.get_yty_data(db, Expense, session)

    yty_data = dict([(i.due_date.strftime('%Y%m%d'), []) for i in db_yty_data])
    for i in db_yty_data:
        yty_data[i.due_date.strftime('%Y%m%d')].append({'expense': i.expense,
                                                        'cost': i.cost,
                                                        'expense_type': i.expense_type
                                                        })
    default_fields = Template.query.filter_by(user_id=session['user_id'],
                                              default=True
                                              ).one()
    default_fields = default_fields.template
    for i in Template.query.filter_by(user_id=session['user_id']).all():
        template_names.append(i.name)
    print(template_names)
    return render_template('index.html', form=form,
                           expenses=yty_data, name=current_user.username,
                           default_fields=default_fields, template_names=template_names)


@main_blueprint.route('/get_template_data', methods=['POST'])
@login_required
def get_template_data():
    if request.method == 'POST':
        template_name = request.json['name']

        temp = Template.query.filter_by(user_id=session['user_id'],
                                        name=template_name
                                        ).one()
        return temp.template


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def handle_needs_login():
    return redirect(url_for('main.login', next=request.endpoint))


def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect_dest(fallback=url_for('main.index'))

        return '<h1>Bad Creds</h1>'
    return render_template('login.html', form=form)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
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

    update_template_form.name.choices = [
        (i.name, i.name) for i in _templates()]

    if update_fields:
        template_list = [i.template for i in _templates() if i.name == _templates()[0].name]
        template_list = ', '.join(map(str, template_list))
        update_template_form.fields.data = template_list


def get_forms(update_fields):
    add_template_form = AddTemplateFrom(request.form, prefix='add_template_')
    update_template_form = UpdateTemplateFrom(
            request.form, prefix='update_template_')
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


@main_blueprint.route('/history', methods=['GET'])
@login_required
def history():
    yty_data = []
    db_yty_data = helper.get_yty_data(db, Expense, session)

    for i in db_yty_data:
        yty_data.append({'id': i.id,
                         'expense': i.expense,
                         'cost': i.cost,
                         'due_date': i.due_date.strftime('%Y-%m-%d'),
                         'type': i.expense_type})

    today = datetime.datetime.now()
    from_date = (today - datetime.timedelta(days=365)).replace(day=1)
    return render_template('history.html', data=yty_data, from_date=from_date, to_date=today)


@main_blueprint.route('/get_history', methods=['POST'])
@login_required
def get_history():
    if request.method == 'POST':
        to_date = request.json['to_date']
        from_date = request.json['from_date']
        yty_data = []

        data = db.session.query(Expense).filter(Expense.due_date >= from_date,
                                                Expense.due_date <= to_date,
                                                Expense.user_id == session['user_id']
                                                ).order_by(Expense.id).all()
        for i in data:
            yty_data.append({'id': i.id,
                             'expense': i.expense,
                             'cost': i.cost,
                             'due_date': i.due_date.strftime('%Y-%m-%d'),
                             'type': i.expense_type})
        return jsonify(yty_data)


@main_blueprint.route('/update_history_row', methods=['POST'])
@login_required
def update_history_row():
    if request.method == 'POST':
        update_data = request.json
        row = Expense.query.filter_by(user_id=session['user_id'],
                                      id=update_data['update_id']
                                      ).first()
        row.expese = update_data['expense']
        row.cost = update_data['cost']
        row.due_date = update_data['due_date']
        row.expense_type = update_data['type']
        db.session.commit()
    return ''


@main_blueprint.route('/get_template_fields', methods=['POST'])
@login_required
def get_fields():
    template_name = request.json['template_name']
    template_row = Template.query.filter_by(name=template_name,
                                            user_id=session['user_id']).first()
    return jsonify({'fields': template_row.template})


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
