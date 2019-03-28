import os, importlib

from flask_login import UserMixin

from expenses import db, ma, config

class Schema():
    region_config = config.os.environ['APP_SETTINGS'].split('.')[2]
    print(f'Running with: {region_config}')
    class_ = getattr(config, region_config)
    schema_name = class_.SCHEMA

class User(UserMixin, db.Model):
    __tabelname__ = 'user'
    __table_args__ = {'schema': Schema.schema_name}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String())

    template = db.relationship('Template', backref='user')
    expense = db.relationship('Expense', backref='user')


class Template(db.Model):
    __tabelname__ = 'template'
    __table_args__ = {'schema': Schema.schema_name}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=False)
    template = db.Column(db.String, unique=False)
    default = db.Column(db.Boolean)

    user_id = db.Column(db.ForeignKey(f'{Schema.schema_name}.user.id'))

    def __init__(self, name, template, default, user_id):
        self.name = name
        self.template = template
        self.default = default
        self.user_id = user_id

    def __repr__(self):
        return f'{self.name} - {self.template} - {self.default} - {self.user_id}'


class Expense(db.Model):
    __tabelname__ = 'expense'
    __table_args__ = {'schema': Schema.schema_name}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expense = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    expense_type = db.Column(db.String, nullable=False)

    user_id = db.Column(db.ForeignKey(f'{Schema.schema_name}.user.id'), nullable=False)

    def __init__(self, expense, cost, due_date, expense_type, user_id):
        self.expense = expense
        self.cost = cost
        self.due_date = due_date
        self.expense_type = expense_type
        self.user_id = user_id

    def __repr__(self):
        return '{} - {} - {} - {}'.format(self.expense, self.cost, self.due_date, self.expense_type)


class ExpensesSchema(ma.ModelSchema):
    class Meta:
        model = Expense
