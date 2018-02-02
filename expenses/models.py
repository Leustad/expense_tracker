from expenses import db


class Expenses(db.Model):
    __tabelname__ = 'expenses'
    __table_args__ = {'schema': 'expenses_dev'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)

    def __init__(self, name='', date='', role=''):
        self.name = name
        self.date = date
        self.role = role

    def __repr__(self):
        return '{} - {} - {}'.format(self.name, self.role, self.date)
