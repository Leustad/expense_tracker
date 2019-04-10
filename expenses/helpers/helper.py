import datetime
import os
from functools import wraps

from flask import url_for, session, redirect
from flask_mail import Message

from expenses import config, mail


def get_data(db, table, session, to_date,
             from_date=(datetime.datetime.now() - datetime.timedelta(days=184)).replace(day=1)):
    data = db.session.query(table).filter(table.due_date >= from_date,
                                          table.due_date <= to_date,
                                          table.user_id == session['user_id']
                                          ).order_by(table.due_date.desc()).all()
    return data


def generate_hist_data(data):
    hist_data = []
    for i in data:
        hist_data.append(
                {'id': i.id,
                 'expense': i.expense,
                 'cost': i.cost,
                 'due_date': i.due_date.strftime('%Y-%m-%d'),
                 'type': i.expense_type}
        )
    return hist_data


def generate_graph_data(data):
    graph_data = {}
    graph_data = dict([(i.due_date.strftime('%Y%m%d'), []) for i in data])

    for i in data:
        graph_data[i.due_date.strftime('%Y%m%d')].append({'expense': i.expense,
                                                          'cost': i.cost,
                                                          'expense_type': i.expense_type
                                                          })
    return graph_data


def get_region_class():
    region_config = config.os.environ['APP_SETTINGS'].split('.')[2]
    return getattr(config, region_config)


def is_user_active(user):
    if user.active:
        return True


def send_activation_email(user):
    token = user.get_token(salt='email-activation-token')
    msg = Message('Account Activation Request',
                  sender=os.environ.get('EMAIL_USERNAME'),
                  recipients=[user.email]
                  )
    msg.body = f'''To activate your account, please visit the following link:
{url_for('main.activate_account', token=token, _external=True)}


if you did not make this request, then simply ignore this email and no change will be made

From Expense-Pro Team with Love <3
'''
    mail.send(msg)


def send_reset_email(user):
    token = user.get_token(salt='password-reset-token')
    msg = Message('Password Reset Request',
                  sender=os.environ.get('EMAIL_USERNAME'),
                  recipients=[user.email]
                  )
    msg.body = f'''To reset our password, visit the following link:
{url_for('main.reset_token', token=token, _external=True)}


if you did not make this request, then simply ignore this email and no change will be made

From Expense-Pro Team with Love <3
'''
    mail.send(msg)


from expenses.models import User


def active_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        user = User.query.filter_by(id=session['user_id']).first()
        if not is_user_active(user):
            return redirect(url_for('main.request_activation'))

        return func(*args, **kwargs)
    return inner
