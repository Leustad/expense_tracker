import datetime


def get_data(db, table, session, to_date, from_date=(datetime.datetime.now() - datetime.timedelta(days=184)).replace(day=1)):
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