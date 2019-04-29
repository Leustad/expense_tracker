from flask import Blueprint, render_template, request, session, url_for, jsonify, flash
from flask_login import login_required
from werkzeug.utils import redirect

from expenses import db
from expenses.helpers.helper import active_required, get_forms, deselect_default, get_user_id
from expenses.models import Template

template_blueprint = Blueprint('template', __name__)


@template_blueprint.route('/template', methods=['GET'])
@login_required
@active_required
def template():
    add_template_form, update_template_form = get_forms(update_fields=True)
    return render_template('template.html',
                           add_template_form=add_template_form,
                           update_template_form=update_template_form)


@template_blueprint.route('/add_template', methods=['POST'])
@login_required
@active_required
def add_template():
    add_template_form, update_template_form = get_forms(update_fields=True)
    if request.method == 'POST' and add_template_form.validate_on_submit():
        template_name = Template.query.filter_by(id=session['user_id'],
                                                 name=add_template_form.name.data
                                                 ).first()
        # If template name doesn't exists
        if not template_name:

            if add_template_form.default.data:
                deselect_default()

            new_template = Template(add_template_form.name.data,
                                    add_template_form.fields.data,
                                    True if add_template_form.default.data else False,
                                    get_user_id()
                                    )
            db.session.add(new_template)
            db.session.commit()
            flash('New Template Added', 'success')
            return redirect(url_for('template.template'))
    return render_template('template.html',
                           add_template_form=add_template_form,
                           update_template_form=update_template_form)


@template_blueprint.route('/update_template', methods=['POST'])
@login_required
@active_required
def update_template():
    add_template_form, update_template_form = get_forms(update_fields=False)

    if request.method == 'POST' and update_template_form.validate_on_submit():
        if update_template_form.default.data:
            deselect_default()

        template_row = Template.query.filter_by(user_id=session['user_id'],
                                                name=update_template_form.name.data).first()

        template_row.name = update_template_form.name.data
        template_row.template = str(update_template_form.fields.data)
        template_row.default = update_template_form.default.data

        # db.session.add(template_row)
        db.session.commit()
        flash('Template Updated', 'success')
        return redirect(url_for('template.template'))
    return render_template('template.html',
                           add_template_form=add_template_form,
                           update_template_form=update_template_form)


@template_blueprint.route('/get_template_fields', methods=['POST'])
@login_required
@active_required
def get_fields():
    template_name = request.json['template_name']
    template_row = Template.query.filter_by(name=template_name,
                                            user_id=session['user_id']).first()
    return jsonify({'fields': template_row.template})
