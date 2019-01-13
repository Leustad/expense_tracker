import json

import datetime
from flask import render_template, redirect, url_for, request, Blueprint, jsonify

from expenses import db
from expenses.forms import ExpensesForm
from expenses.models import Expenses, ExpensesSchema

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
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
                print('asd', entry)
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
    return render_template('index.html', form=form, expenses=output, dates=dates)
