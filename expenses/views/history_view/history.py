import datetime

from flask import Blueprint, session, render_template, request, jsonify
from flask_login import login_required

from expenses import db
from expenses.helpers.helper import active_required, get_data, generate_hist_data, generate_graph_data
from expenses.models import Expense

history_blueprint = Blueprint('history', __name__)


@history_blueprint.route('/history', methods=['GET'])
@login_required
@active_required
def history():
    yty_data = []
    today = datetime.datetime.now()
    six_months = get_data(db, Expense, session, today)

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


@history_blueprint.route('/get_history', methods=['POST'])
@login_required
@active_required
def get_history():
    if request.method == 'POST':
        to_date = request.json['to_date']
        from_date = request.json['from_date']
        hist_data = []

        data = get_data(db, Expense, session, to_date, from_date)
        hist_data = generate_hist_data(data)
        graph_data = generate_graph_data(data)

        return jsonify(
                {'hist_data': hist_data,
                 'graph_yty_data': graph_data}
        )


@history_blueprint.route('/update_history_row', methods=['POST'])
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

        data = get_data(db, Expense, session, to_date, from_date)
        hist_data = generate_hist_data(data)
        graph_data = generate_graph_data(data)

        return jsonify(
                {'hist_data': hist_data,
                 'graph_yty_data': graph_data}
        )


@history_blueprint.route('/delete_hist_row', methods=['POST'])
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

        data = get_data(db, Expense, session, to_date, from_date)
        hist_data = generate_hist_data(data)
        graph_data = generate_graph_data(data)
        return jsonify(
                {'hist_data': hist_data,
                 'graph_yty_data': graph_data}
        )
