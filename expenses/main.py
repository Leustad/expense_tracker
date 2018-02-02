# import json
# from datetime import datetime
# from functools import wraps

from flask import render_template, session, flash, redirect, url_for, request, Blueprint, app
from sqlalchemy.exc import IntegrityError

from expenses.forms import ExpensesForm
from expenses.models import Expenses

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = ExpensesForm(request.form)
    # messages = db.session.query(MessageBoard).order_by(MessageBoard.id).limit(20)
    #
    return render_template('index.html', form=form)
