from wtforms import (
    FieldList, Form, FormField, BooleanField, DateTimeField,
    DecimalField, HiddenField, IntegerField, SelectField, StringField,
    PasswordField, RadioField, TextAreaField
)
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from .enums import (
    UserRole, ESTADOS_ACTIVIDAD, ESTILOS_ACTIVIDAD, ESPACIAMIENTOS,
    TIPOS_MOVIMIENTO, HUMEDADES, PLASTICIDADES, ORIGENES_SUELO,
    VELOCIDADES, MODOS_MORFM, SEVERIDADES_MORFM)
from .models.movimiento import Mapa, Foto, DetalleLitologia
from .validators import UserExists


class IdField(HiddenField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = int(valuelist[0])
        else:
            self.data = None


class NullableIntegerField(IntegerField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            super(NullableIntegerField, self).process_formdata(valuelist)
        else:
            self.data = None


class NullableDecimalField(DecimalField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            super(NullableDecimalField, self).process_formdata(valuelist)
        else:
            self.data = None


class CustomFieldList(FieldList):
    def __init__(self, unbound_field, obj_ctor, label=None, validators=None,
                 min_entries=0, max_entries=None, default=tuple(), **kwargs):

        super(CustomFieldList, self).__init__(unbound_field, label,
                                              validators, min_entries,
                                              max_entries, default, **kwargs)

        self.obj_ctor = obj_ctor

    def populate_obj(self, obj, name):
        values = getattr(obj, name, None)

        self.prepare_list(values)
        super(CustomFieldList, self).populate_obj(obj, name)

    def prepare_list(self, obj_list):
        # eliminar los objetos que no están en el formulario
        for obj in obj_list:
            exists = any(fields['id'].data == obj.id for fields in self)

            if not exists:
                obj_list.remove(obj)

        # insertar los elementos agregados en el formulario en el mismo orden
        i = 0
        for fields in self:
            # los nuevos elementos no tienen id
            if not fields['id'].data:
                obj_list.insert(i, self.obj_ctor())

            i = i + 1


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


class MapaForm(Form):
    id = IdField()

    nro_mapa = StringField()
    anio = StringField(validators=[Length(max=4)])
    escala = StringField()
    editor = StringField()


class FotoForm(Form):
    id = IdField()

    nro_foto = StringField()
    anio = StringField(validators=[Length(max=4)])
    escala = StringField()
    editor = StringField()


class LocalizacionForm(Form):
    id = IdField()

    pais = StringField()
    provincia = StringField()
    ciudad = StringField()
    localidad = StringField()

    sitio = StringField()
    norte = NullableIntegerField()
    este = NullableIntegerField()
    proyeccion = StringField()
    altura = NullableIntegerField()

    ref_geograficos = TextAreaField()

    mapas = CustomFieldList(FormField(MapaForm), Mapa)
    fotos = CustomFieldList(FormField(FotoForm), Foto)


class DistribucionForm(Form):
    id = IdField()

    retrogresivo = BooleanField()
    avanzado = BooleanField()
    ensanchado = BooleanField()
    confinado = BooleanField()
    creciente = BooleanField()
    decreciente = BooleanField()
    movil = BooleanField()


class ActividadForm(Form):
    id = IdField()

    primera_fecha = DateTimeField(format='%Y-%m-%d')
    ultima_fecha = DateTimeField(format='%Y-%m-%d')

    edad = StringField(validators=[Length(max=4)])
    estado = RadioField(choices=ESTADOS_ACTIVIDAD,
                        coerce=int,
                        validators=[DataRequired()])

    estilo = RadioField(choices=ESTILOS_ACTIVIDAD,
                        coerce=int,
                        validators=[DataRequired()])

    distribucion = FormField(DistribucionForm)


class DetalleLitologiaForm(Form):
    id = IdField()

    estructura = StringField(validators=[Length(max=128)])
    dir_buzamiento = StringField(validators=[Length(max=64)])
    buzamiento = StringField(validators=[Length(max=64)])
    espaciamiento = RadioField(choices=[(i, '') for i in ESPACIAMIENTOS])


class LitologiaForm(Form):
    id = IdField()

    descripcion = TextAreaField()
    detalles = CustomFieldList(FormField(DetalleLitologiaForm),
                               DetalleLitologia)


class ClasificacionForm(Form):
    id = IdField()

    sistema = StringField(validators=[Length(max=128)])
    nombre = StringField(validators=[Length(max=128)])

    tipo_uno = RadioField(choices=TIPOS_MOVIMIENTO)
    tipo_dos = RadioField(choices=TIPOS_MOVIMIENTO)

    roca_uno = NullableIntegerField()
    roca_dos = NullableIntegerField()
    detritos_uno = NullableIntegerField()
    detritos_dos = NullableIntegerField()
    tierra_uno = NullableIntegerField()
    tierra_dos = NullableIntegerField()

    bloques_uno = NullableIntegerField()
    bloques_dos = NullableIntegerField()
    cantos_uno = NullableIntegerField()
    cantos_dos = NullableIntegerField()
    grava_uno = NullableIntegerField()
    grava_dos = NullableIntegerField()
    arena_uno = NullableIntegerField()
    arena_dos = NullableIntegerField()
    finos_uno = NullableIntegerField()
    finos_dos = NullableIntegerField()
    organica_uno = NullableIntegerField()
    organica_dos = NullableIntegerField()

    humedad_uno = RadioField(choices=HUMEDADES)
    humedad_dos = RadioField(choices=HUMEDADES)

    plasticidad_uno = RadioField(choices=PLASTICIDADES)
    plasticidad_dos = RadioField(choices=PLASTICIDADES)

    origen = RadioField(choices=ORIGENES_SUELO)

    uscs = TextAreaField()

    canalizado = BooleanField()
    no_canalizado = BooleanField()
    licuacion = BooleanField()
    otra_caracteristica = StringField(validators=[Length(max=128)])

    velocidad = RadioField(choices=VELOCIDADES)
    vmax = StringField(validators=[Length(max=128)])
    vmedia = StringField(validators=[Length(max=128)])


class MorfometriaForm(Form):
    id = IdField()

    dif_corona_punta = NullableDecimalField(places=2)
    long_corona_punta = NullableDecimalField(places=2)
    fahrboschung = NullableDecimalField(places=2)
    pre_falla = NullableDecimalField(places=2)
    post_falla = NullableDecimalField(places=2)
    direccion = StringField(validators=[Length(max=16)])
    azimut = NullableDecimalField(places=2)

    profundidad_falla = NullableDecimalField(places=2)
    ancho_falla = NullableDecimalField(places=2)
    longitud_falla = NullableDecimalField(places=2)
    espesor_masa = NullableDecimalField(places=2)
    ancho_masa = NullableDecimalField(places=2)
    longitud_masa = NullableDecimalField(places=2)
    longitud_total = NullableDecimalField(places=2)
    volumen_inicial = NullableDecimalField(places=2)
    volumen_desplazado = NullableDecimalField(places=2)
    area_inicial = NullableDecimalField(places=2)
    area_total = NullableDecimalField(places=2)
    distancia_viaje = NullableDecimalField(places=2)
    runup = NullableDecimalField(places=2)

    modo = RadioField(choices=MODOS_MORFM)
    severidad = RadioField(choices=SEVERIDADES_MORFM)


class MovimientoForm(Form):
    encuestador = StringField(validators=[DataRequired()])
    fecha = DateTimeField(format='%Y-%m-%d')
    institucion = StringField()
    codigo = StringField(validators=[DataRequired()])

    localizacion = FormField(LocalizacionForm)
    actividad = FormField(ActividadForm)
    litologia = FormField(LitologiaForm)
    clasificacion = FormField(ClasificacionForm)
    morfometria = FormField(MorfometriaForm)
