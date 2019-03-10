import datetime


def get_yty_data(db, table, session):
    return db.session.query(table).filter(table.due_date >= (datetime.datetime.now() - datetime.timedelta(days=365)).replace(day=1),
                                            table.user_id == session['user_id']
                                            )
