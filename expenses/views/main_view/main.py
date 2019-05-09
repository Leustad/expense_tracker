import datetime

from flask import request, url_for, session, render_template, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from expenses import db
from expenses.forms import ExpensesForm
from expenses.helpers.helper import active_required, get_user_id, get_data
from expenses.models import Expense, Template

main_blueprint = Blueprint('main', __name__)


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
    
    six_months = get_data(db, Expense, session, today)

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


@main_blueprint.route('/get_template_data', methods=['POST'])
@login_required
def get_template_data():
    if request.method == 'POST':
        template_name = request.json['name']

        temp = Template.query.filter_by(user_id=session['user_id'],
                                        name=template_name
                                        ).one()
        return temp.template
