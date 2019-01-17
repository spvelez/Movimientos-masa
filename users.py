from flask import (
     Blueprint, flash, render_template, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.validators import StopValidation
from .models.user import User
from .database import session
from .forms import UserForm

bp = Blueprint('users', __name__, template_folder='templates')


@bp.route('/users')
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@bp.route('/users/create', methods=['GET', 'POST'])
def create():
    form = UserForm(request.form)
    form.login.validators.append(UserExists())

    if request.method == 'POST' and form.validate():
        usr = User()
        form.populate_obj(usr)

        usr.password = generate_password_hash(usr.password)
        usr.role = 2
        session.add(usr)
        session.commit()

        return redirect(url_for('.index'))

    return render_template('/users/form.html', form=form)


@bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.filter(User.id == id).first()

    formData = request.form if request.method == 'POST' else None
    form = UserForm(formData, obj=user)

    form.login.validators.append(UserExists(user.id))

    if request.method == 'POST' and form.validate():
        form.populate_obj(user)

        usr.password = generate_password_hash(usr.password)
        session.commit()

        return redirect(url_for('.index'))

    return render_template('/users/form.html', form=form, id=id)


@bp.route('/users/delete/<int:id>', methods=['POST'])
def delete(id):
    usr = User.query.filter(User.id == id).first()
    session.delete(usr)
    session.commit()

    return redirect(url_for('.index'))


class UserExists:
    def __init__(self, user_id=0, message=None):
        self.user_id = user_id

        if not message:
            message = 'El usuario ya existe'
        self.message = message

    def __call__(self, form, field):
        count = User.query.filter(User.id != self.user_id,
                                  User.login == field.data).count()

        if count > 0:
            raise StopValidation(self.message)
