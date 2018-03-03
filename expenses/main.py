# import json
# from datetime import datetime
# from functools import wraps

from flask import render_template, redirect, url_for, request, Blueprint

from expenses import db
from expenses.forms import ExpensesForm
from expenses.models import Expenses


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = ExpensesForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            for n in range(len(form.expense_name.raw_data)):
                if form.expense_name.raw_data[n] != '':
                    data = Expenses(form.expense_name.raw_data[n].title(),
                                    form.cost.raw_data[n],
                                    form.month.raw_data[n] + form.year.raw_data[n],
                                    form.type.raw_data[n].title(),
                                    )
                    db.session.add(data)
                    db.session.commit()
    return render_template('index.html', form=form)
