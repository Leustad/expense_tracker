import datetime


def get_six_months_data(db, table, session):
    return db.session.query(table).filter(table.due_date >= (datetime.datetime.now() - datetime.timedelta(days=184)).replace(day=1),
                                            table.user_id == session['user_id']
                                            ).order_by(table.due_date.desc()).all()
