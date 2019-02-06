from flask import (
     Blueprint, flash, jsonify, render_template, redirect, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from masas import authorize
from masas.enums import UserRole
from masas.models.user import User
from masas.core.database import db_session
from masas.forms import UserForm
from masas.repositories.userrepo import UserRepository


bp = Blueprint('users', __name__, template_folder='templates')
user_repo = UserRepository()


@bp.route('/users')
@authorize(UserRole.admin)
def index():
    if not request.is_xhr:
        return render_template('users/index.html')

    search = request.args.get('queries[search]', '')
    limit = request.args.get('perPage', 0)
    offset = request.args.get('offset', 0)

    users = user_repo.get_list(search, limit, offset)

    def format_user(user):
        role = UserRole.from_value(user.role)
        return {
            'id': user.id,
            'login': user.login,
            'name': user.name,
            'role': role.value[1]
        }

    return jsonify({
        'registros': [format_user(u) for u in users[1]],
        'total': users[0]
    })


@bp.route('/users/create', methods=['GET', 'POST'])
@authorize(UserRole.admin)
def create():
    form = UserForm(request.form)
    form.user_id = 0

    if request.method == 'POST' and form.validate():
        usr = User()
        form.populate_obj(usr)

        usr.password = generate_password_hash(usr.password)
        user_repo.persist(usr)

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
        user_repo.persist(user)

        return redirect(url_for('.index'))

    return render_template('/users/form.html', form=form, id=id)


@bp.route('/users/delete/<int:id>', methods=['POST'])
@authorize(UserRole.admin)
def delete(id):
    usr = user_repo.get_by_id(id)
    user_repo.delete(usr)

    return redirect(url_for('.index'))
