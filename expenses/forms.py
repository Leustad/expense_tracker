import datetime
import decimal

from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, FormField, FieldList, PasswordField, BooleanField, \
    TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Email, Length, ValidationError
from wtforms import Form as NoCsrfForm

from expenses.models import Template


def check_numeric(form, field):
    try:
        decimal.Decimal(field)
    except:
        ValidationError('This field requires a numeric value')


class ExpenseItem(NoCsrfForm):
    expense = StringField('Expense_Item', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[check_numeric])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    desc = SelectField('Role', choices=[('Mutual', 'Mutual'),
                                        ('Personal', 'Personal'),
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


def field_count_check(form, field):
    if len(str(field).split(',')) < 1:
        raise ValidationError('Must Have at least 1 Comma Separated Field Name')


class AddTemplateFrom(FlaskForm):
    name = StringField('template name', validators=[DataRequired(), Length(min=4, max=50)])
    fields = TextAreaField('fields', validators=[DataRequired(), field_count_check])
    default = BooleanField('default')


class UpdateTemplateFrom(FlaskForm):
    name = SelectField('template name', validators=[DataRequired()])
    fields = TextAreaField('fields', validators=[DataRequired(), field_count_check])
    default = BooleanField('default')


# class HistoryItem(NoCsrfForm):
#     from_date = DateField('from_date', validators=[DataRequired()])
#     to_date = DateField('to_date', validators=[DataRequired()])


# class MetaHistory(HistoryItem, ExpenseItem):
#     pass


# class HistoryForm(FlaskForm):
#     items = FieldList(FormField(MetaHistory), min_entries=1)