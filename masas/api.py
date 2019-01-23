from flask import (
     Blueprint, make_response, request, jsonify
)
from werkzeug.exceptions import NotFound
from .enums import UserRole
from .models.user import User
from .database import session

bp = Blueprint('api', __name__)


def format_user(user):
    role = UserRole.from_value(user.role)
    return {
        'id': user.id,
        'login': user.login,
        'name': user.name,
        'role': role.value[1]
    }


@bp.route('/api/users')
def all_users():
    users = User.query.all()

    return jsonify([format_user(u) for u in users])


@bp.route('/api/users/<int:id>')
def user(id):
    user = User.query.filter(User.id == id).first()

    if (user is None):
        raise NotFound('No existe el usuario con id %d' % id)

    return jsonify(format_user(user))


@bp.errorhandler(404)
def not_found(e):
    return make_response(jsonify({'error': e.description}), 404)
