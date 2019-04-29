from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from expenses import db, ma, config

from flask_login import UserMixin


def get_region_class():
    region_config = config.os.environ['APP_SETTINGS'].split('.')[2]
    return getattr(config, region_config)


class Schema(object):
    schema_name = get_region_class().SCHEMA


class User(UserMixin, db.Model):
    __tabelname__ = 'user'
    __table_args__ = {'schema': Schema.schema_name}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String())
    last_login = db.Column(db.DateTime)
    active = db.Column(db.Boolean)

    template = db.relationship('Template', backref='user')
    expense = db.relationship('Expense', backref='user')

    def get_token(self, salt, expires_sec=1800):
        s = Serializer(get_region_class().SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}, salt=f'{salt}').decode('utf-8')

    @staticmethod
    def verify_token(token, salt):
        s = Serializer(get_region_class().SECRET_KEY)
        try:
            user_id = s.loads(token, salt=f'{salt}')['user_id']
        except:
            return None
        return User.query.get(user_id)


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
