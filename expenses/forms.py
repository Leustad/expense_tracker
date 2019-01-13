import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, FormField, FieldList
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
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
