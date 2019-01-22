from wtforms import (
    Form, BooleanField, SelectField,
    StringField, PasswordField, TextAreaField
)
from wtforms.validators import DataRequired, EqualTo
from .validators import UserExists


class UserForm(Form):
    name = StringField('Nombre', [DataRequired()])
    login = StringField('Login', [DataRequired(), UserExists()])
    password = PasswordField('Contraseña', [
        DataRequired(),
        EqualTo('confirm_password', 'Las contraseñas deben coincidir')])
    confirm_password = PasswordField('Confirma la contraseña')
