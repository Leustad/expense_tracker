import datetime

from flask import render_template, redirect, url_for, request, Blueprint, jsonify, session, flash
from flask_login import login_required, login_user, current_user, logout_user

from expenses.helpers import helper
from expenses import db, bcrypt, login_manager
from expenses.forms import (ExpensesForm, LoginForm, RegisterForm, AddTemplateFrom, UpdateTemplateFrom,
                            RequestResetFrom, ResetPasswordFrom, RequestActivationForm)
from expenses.helpers.helper import active_required
from expenses.models import Expense, User, Template

main_blueprint = Blueprint('main', __name__)


def get_user_id():
    return User.query.filter_by(id=session['user_id']).first().id


@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@active_required
def index():
    template_names = []
    default_fields = None
    form = ExpensesForm(request.form)
    default_template_name = ''
    today = datetime.datetime.now()

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
    six_months = helper.get_data(db, Expense, session, today)

    yty_data = dict([(i.due_date.strftime('%Y%m%d'), []) for i in six_months])
    for i in six_months:
        yty_data[i.due_date.strftime('%Y%m%d')].append({'expense': i.expense,
                                                        'cost': i.cost,
                                                        'expense_type': i.expense_type
                                                        })
    try:
        default_fields = Template.query.filter_by(user_id=session['user_id'],
                                                  default=True
                                                  ).one()
        default_template_name = default_fields.name
        default_fields = default_fields.template

    except Exception as e:
        print(e)

    for i in Template.query.filter_by(user_id=session['user_id']).all():
        template_names.append(i.name)
    return render_template('index.html', form=form,
                           expenses=yty_data, name=current_user.username,
                           default_fields=default_fields, template_names=template_names,
                           default_template_name=default_template_name)


@main_blueprint.route('/request_activation', methods=['GET', 'POST'])
def request_activation():
    form = RequestActivationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.active:
            flash('Account Already Active. No Need to re-activate')
            return redirect(url_for('main.index'))
        helper.send_activation_email(user)
        flash(f'Activation Email has been sent to {user.email}. Please don\'t forget to check your spam folder', 'text-info')
        return render_template('info.html',
                               title='Info',
                               msg='Account Activation has been Requested.'
                               )
    else:
        return render_template('request_activation.html', form=form, title='Request Activation')


@main_blueprint.route('/request_activation/<token>', methods=['GET', 'POST'])
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

        flash('Invalid/Wrong Credentials. Please try again.')
    return render_template('login.html', form=form)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                        )
        db.session.add(new_user)
        db.session.commit()
        flash('Please check your email for an activation link', 'info')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


@main_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetFrom(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        helper.send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('main.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@main_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_token(token, salt='password-reset-token')

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.reset_request'))
    form = ResetPasswordFrom()
    if form.validate_on_submit():
        hashed_psw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_psw
        db.session.commit()
        flash('Your password has been updated !! You are now able to login with your new password.')
        return redirect(url_for('main.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


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
    update_template_form = UpdateTemplateFrom(request.form, prefix='update_template_')
    ready_update_template_form(update_template_form, update_fields)
    return add_template_form, update_template_form


@main_blueprint.route('/template', methods=['GET'])
@login_required
@active_required
def template():
    add_template_form, update_template_form = get_forms(update_fields=True)
    return render_template('template.html',
                           add_template_form=add_template_form,
                           update_template_form=update_template_form)


@main_blueprint.route('/add_template', methods=['POST'])
@login_required
@active_required
def add_template():
    add_template_form, update_template_form = get_forms(update_fields=True)
    if request.method == 'POST' and add_template_form.validate_on_submit():
        template_name = Template.query.filter_by(id=session['user_id'],
                                                 name=add_template_form.name.data
                                                 ).first()
        # If template name doesn't exists
        if not template_name:

            if add_template_form.default.data:
                deselect_default()

            new_template = Template(add_template_form.name.data,
                                    add_template_form.fields.data,
                                    True if add_template_form.default.data else False,
                                    get_user_id()
                                    )
            db.session.add(new_template)
            db.session.commit()
            return redirect(url_for('main.template'))
    return render_template('template.html',
                           add_template_form=add_template_form,
                           update_template_form=update_template_form)


@main_blueprint.route('/update_template', methods=['POST'])
@login_required
@active_required
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
        return redirect(url_for('main.template'))
    for fieldName, errorMessages in update_template_form.errors.items():
        for err in errorMessages:
            print(err)
    return render_template('template.html',
                           add_template_form=add_template_form,
                           update_template_form=update_template_form)


@main_blueprint.route('/history', methods=['GET'])
@login_required
@active_required
def history():
    yty_data = []
    today = datetime.datetime.now()
    six_months = helper.get_data(db, Expense, session, today)

    for i in six_months:
        yty_data.append({'id': i.id,
                         'expense': i.expense,
                         'cost': i.cost,
                         'due_date': i.due_date.strftime('%Y-%m-%d'),
                         'type': i.expense_type})

    graph_yty_data = dict([(i.due_date.strftime('%Y%m%d'), [])
                           for i in six_months])

    for i in six_months:
        graph_yty_data[i.due_date.strftime('%Y%m%d')].append({'expense': i.expense,
                                                              'cost': i.cost,
                                                              'expense_type': i.expense_type
                                                              })

    from_date = (today - datetime.timedelta(5 * 365 / 12)).replace(day=1)
    return render_template('history.html', data=yty_data,
                           graph_yty_data=graph_yty_data,
                           from_date=from_date,
                           to_date=today)


@main_blueprint.route('/get_history', methods=['POST'])
@login_required
@active_required
def get_history():
    if request.method == 'POST':
        to_date = request.json['to_date']
        from_date = request.json['from_date']
        hist_data = []

        data = helper.get_data(db, Expense, session, to_date, from_date)
        hist_data = helper.generate_hist_data(data)
        graph_data = helper.generate_graph_data(data)

        return jsonify(
                {'hist_data': hist_data,
                 'graph_yty_data': graph_data}
        )


@main_blueprint.route('/update_history_row', methods=['POST'])
@login_required
@active_required
def update_history_row():
    if request.method == 'POST':
        hist_data = []
        to_date = request.json['to_date']
        from_date = request.json['from_date']
        update_data = request.json['update_data']
        row = Expense.query.filter_by(user_id=session['user_id'],
                                      id=update_data['update_id']
                                      ).first()
        row.expense = update_data['expense']
        row.cost = update_data['cost']
        row.due_date = update_data['due_date']
        row.expense_type = update_data['type']
        db.session.commit()

        data = helper.get_data(db, Expense, session, to_date, from_date)
        hist_data = helper.generate_hist_data(data)
        graph_data = helper.generate_graph_data(data)

        return jsonify(
                {'hist_data': hist_data,
                 'graph_yty_data': graph_data}
        )


@main_blueprint.route('/delete_hist_row', methods=['POST'])
@login_required
@active_required
def delete_hist_row():
    if request.method == 'POST':
        to_date = request.json['to_date']
        from_date = request.json['from_date']
        row_id = request.json['row_id']

        row = Expense.query.filter_by(user_id=session['user_id'],
                                      id=row_id
                                      ).first()

        print('Deleting: ', row)
        db.session.delete(row)
        db.session.commit()

        data = helper.get_data(db, Expense, session, to_date, from_date)
        hist_data = helper.generate_hist_data(data)
        graph_data = helper.generate_graph_data(data)
        return jsonify(
                {'hist_data': hist_data,
                 'graph_yty_data': graph_data}
        )


@main_blueprint.route('/get_template_fields', methods=['POST'])
@login_required
@active_required
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
