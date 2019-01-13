from expenses import db, ma


class Expenses(db.Model):
    __tabelname__ = 'expenses'
    __table_args__ = {'schema': 'leustad'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expense = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    expense_type = db.Column(db.String, nullable=False)

    def __init__(self, expense, cost, due_date, expense_type):
        self.expense = expense
        self.cost = cost
        self.due_date = due_date
        self.expense_type = expense_type

    def __repr__(self):
        return '{} - {} - {} - {}'.format(self.expense, self.cost, self.due_date, self.expense_type)


class ExpensesSchema(ma.ModelSchema):
    class Meta:
        model = Expenses
