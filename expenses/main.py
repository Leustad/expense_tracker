import datetime

from flask import render_template, redirect, url_for, request, Blueprint, jsonify, session, flash
from flask_login import login_required, login_user, current_user, logout_user

from expenses.helpers import helper
from expenses import db, bcrypt, login_manager
from expenses.forms import (ExpensesForm, LoginForm, RegisterForm, AddTemplateFrom, UpdateTemplateFrom,
                            RequestResetFrom, ResetPasswordFrom, RequestActivationForm)
from expenses.helpers.helper import active_required
from expenses.models import Expense, User, Template


