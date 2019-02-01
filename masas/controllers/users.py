from flask import (
     Blueprint, flash, render_template, redirect, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from masas import authorize
from masas.enums import UserRole
from masas.models.user import User
from masas.database import db_session
from masas.forms import UserForm

bp = Blueprint('users', __name__, template_folder='templates')


@bp.route('/users')
@authorize(UserRole.admin)
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@bp.route('/users/create', methods=['GET', 'POST'])
@authorize(UserRole.admin)
def create():
    form = UserForm(request.form)
    form.user_id = 0

    if request.method == 'POST' and form.validate():
        usr = User()
        form.populate_obj(usr)

        usr.password = generate_password_hash(usr.password)
        db_session.add(usr)
        db_session.commit()

        return redirect(url_for('.index'))

    return render_template('/users/form.html', form=form)


@bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@authorize(UserRole.admin)
def edit(id):
    user = User.query.filter(User.id == id).first()

    formData = request.form if request.method == 'POST' else None
    form = UserForm(formData, obj=user)
    form.user_id = id

    if request.method == 'POST' and form.validate():
        form.populate_obj(user)

        user.password = generate_password_hash(user.password)
        db_session.commit()

        return redirect(url_for('.index'))

    return render_template('/users/form.html', form=form, id=id)


@bp.route('/users/delete/<int:id>', methods=['POST'])
@authorize(UserRole.admin)
def delete(id):
    usr = User.query.filter(User.id == id).first()
    db_session.delete(usr)
    db_session.commit()

    return redirect(url_for('.index'))
