import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, FormField, FieldList, PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Email, Length
from wtforms import Form as NoCsrfForm


class ExpenseItem(NoCsrfForm):
    expense = StringField('Expense_Item', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()],
                         default=datetime.datetime.today().date())
    desc = SelectField('Role', choices=[('mutual', 'Mutual'),
                                        ('personal#1', 'Personal #1'),
                                        ('personal#2', 'Personal #2')
                                        ])


class ExpensesForm(FlaskForm):
    """A collection of expense items."""
    items = FieldList(FormField(ExpenseItem), min_entries=1)


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=4, max=80)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=4, max=80)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])
