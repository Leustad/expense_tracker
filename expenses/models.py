from expenses import db


class Expenses(db.Model):
    __tabelname__ = 'expenses'
    __table_args__ = {'schema': 'expenses_dev'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=False, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.String, nullable=False)
    expense_type = db.Column(db.String, nullable=False)

    def __init__(self, name='', cost='', date='', expense_type=''):
        self.name = name
        self.cost = cost
        self.date = date
        self.expense_type = expense_type

    def __repr__(self):
        return '{} - {} - {} - {}'.format(self.name, self.cost, self.expense_type, self.date)
