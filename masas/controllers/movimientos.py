from flask import (
     Blueprint, flash, render_template, redirect, request, session, url_for
)
from masas.database import session
from masas.enums import ESPACIAMIENTOS
from masas.forms import MovimientoForm
from masas.models.movimiento import (
    Movimiento, Localizacion, Mapa, Foto, Actividad, Distribucion, Litologia,
    Clasificacion, Morfometria)

bp = Blueprint('movimientos', __name__, template_folder='templates')


@bp.route('/movimientos')
def index():
    lista = Movimiento.query.all()
    return render_template('movimientos/index.html', movimientos=lista)


@bp.route('/movimientos/create', methods=['GET', 'POST'])
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

        form.populate_obj(mov)

        session.add(mov)
        session.commit()

        return redirect(url_for('.index'))

    return render_template('movimientos/form.html',
                           form=form,
                           espaciamientos=ESPACIAMIENTOS)


@bp.route('/movimientos/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mov = Movimiento.query.filter(Movimiento.id == id).first()
    formData = request.form if request.method == 'POST' else None
    form = MovimientoForm(formData, obj=mov)

    if request.method == 'POST' and form.validate():
        form.populate_obj(mov)

        session.commit()
        return redirect(url_for('.index'))

    return render_template('/movimientos/form.html',
                           form=form,
                           espaciamientos=ESPACIAMIENTOS)


@bp.route('/movimientos/delete/<int:id>', methods=['POST'])
def delete(id):
    mov = Movimiento.query.filter(Movimiento.id == id).first()
    session.delete(mov)
    session.commit()

    return redirect(url_for('.index'))
