from wtforms import (
    FieldList, Form, FormField, BooleanField, DateTimeField, HiddenField,
    IntegerField, SelectField, StringField, PasswordField, TextAreaField
)
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from .enums import UserRole
from .validators import UserExists


class UserForm(Form):
    name = StringField('Nombre', [DataRequired()])
    login = StringField('Login', [DataRequired(), UserExists()])
    password = PasswordField('Contraseña', [
        DataRequired(),
        EqualTo('confirm_password', 'Las contraseñas deben coincidir')])
    confirm_password = PasswordField('Confirma la contraseña')
    role = SelectField(coerce=int, choices=[e.value for e in UserRole])


class ChangePasswordForm(Form):
    password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[
        DataRequired(),
        EqualTo('confirm_password', 'Las contraseñas deben coincidir')])
    confirm_password = PasswordField()

    def validate_new_password(form, field):
        if field.data == form.password.data:
            raise ValidationError('La nueva contraseña debe ser distinta')
