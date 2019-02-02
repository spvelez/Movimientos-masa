from flask import (
     Blueprint, flash, render_template, redirect, request, session, url_for
)
from masas import authorize
from masas.database import db_session
from masas.enums import ESPACIAMIENTOS, UserRole
from masas.forms import MovimientoForm
from masas.models.movimiento import (
    Movimiento, Localizacion, Mapa, Foto, Actividad, Distribucion, Litologia,
    Clasificacion, Morfometria, Causa, CoberturaSuelo, UsoSuelo,
    EfectoSecundario, Dano)

bp = Blueprint('movimientos', __name__, template_folder='templates')


@bp.route('/movimientos')
@authorize()
def index():
    lista = Movimiento.query.all()
    return render_template('movimientos/index.html', movimientos=lista)


@bp.route('/movimientos/create', methods=['GET', 'POST'])
@authorize(UserRole.user)
def create():
    form = MovimientoForm(request.form)

    if request.method == 'POST' and form.validate():
        mov = Movimiento()
        mov.localizacion = Localizacion()
        mov.localizacion.mapas = []
        mov.localizacion.fotos = []
        mov.actividad = Actividad()
        mov.actividad.distribucion = Distribucion()
        mov.litologia = Litologia()
        mov.litologia.detalles = []
        mov.clasificacion = Clasificacion()
        mov.morfometria = Morfometria()
        mov.causa = Causa()
        mov.cobertura_suelo = CoberturaSuelo()
        mov.uso_suelo = UsoSuelo()
        mov.documentos_ref = []
        mov.efecto_secundario = EfectoSecundario()
        mov.dano = Dano()
        mov.dano.detalles = []

        form.populate_obj(mov)

        mov.usuario_id = session['user_id']

        db_session.add(mov)
        db_session.commit()

        return redirect(url_for('.index'))

    return render_template('movimientos/form.html',
                           form=form,
                           espaciamientos=ESPACIAMIENTOS)


@bp.route('/movimientos/edit/<int:id>', methods=['GET', 'POST'])
@authorize(UserRole.user)
def edit(id):
    mov = Movimiento.query.filter(Movimiento.id == id).first()
    formData = request.form if request.method == 'POST' else None
    form = MovimientoForm(formData, obj=mov)

    if request.method == 'POST' and form.validate():
        print('embalse: ', form.causa.embalse.data)
        form.populate_obj(mov)

        db_session.commit()
        return redirect(url_for('.index'))

    return render_template('/movimientos/form.html',
                           form=form,
                           espaciamientos=ESPACIAMIENTOS)


@bp.route('/movimientos/delete/<int:id>', methods=['POST'])
@authorize(UserRole.user)
def delete(id):
    mov = Movimiento.query.filter(Movimiento.id == id).first()
    db_session.delete(mov)
    db_session.commit()

    return redirect(url_for('.index'))


@bp.route('/movimientos/view/<int:id>')
@authorize(UserRole.user)
def view(id):
    movimiento = Movimiento.query.filter(Movimiento.id == id).first()

    import masas.enums

    return render_template('/movimientos/view.html',
                           mov=movimiento,
                           enums=masas.enums)
