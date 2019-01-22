from wtforms.validators import StopValidation
from .models.user import User


class UserExists:
    def __init__(self, message=None):
        if not message:
            message = 'El usuario ya existe'
        self.message = message

    def __call__(self, form, field):
        count = User.query.filter(User.id != form.user_id,
                                  User.login == field.data).count()

        if count > 0:
            raise StopValidation(self.message)
