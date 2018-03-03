from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import DataRequired

import time


class ExpensesForm(FlaskForm):
    expense_name = StringField('Expense_Item', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()], default=time.strftime("%Y"))
    month = SelectField('Month', choices=[('Jan', 'January'),
                                          ('Feb', 'February'),
                                          ('Mar', 'March'),
                                          ('Apr', 'April'),
                                          ('May', 'May'),
                                          ('Jun', 'June'),
                                          ('Jul', 'July'),
                                          ('Aug', 'August'),
                                          ('Sep', 'September'),
                                          ('Oct', 'October'),
                                          ('Nov', 'November'),
                                          ('Dec', 'December')
                                          ], validators=[DataRequired()])
    type = SelectField('Role', choices=[('mutual', 'Mutual'),
                                        ('personal#1', 'Personal #1'),
                                        ('personal#2', 'Personal #2')
                                        ])
