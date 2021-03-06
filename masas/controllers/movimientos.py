from flask import (
     Blueprint, flash, current_app, jsonify, render_template,
     redirect, request, session, url_for
)
from weasyprint import HTML
import masas.enums
from masas import authorize
from masas.core.observers import CreateObserver, DeleteObserver
from masas.enums import ESPACIAMIENTOS, UserRole
from masas.forms import MovimientoForm
from masas.models.movimiento import (
    Movimiento, Localizacion, Mapa, Foto, Actividad, Distribucion, Litologia,
    Clasificacion, Morfometria, Causa, CoberturaSuelo, UsoSuelo,
    EfectoSecundario, Dano)
from masas.repositories.movimientorepo import MovimientoRepository

bp = Blueprint('movimientos', __name__, template_folder='templates')
mov_repo = MovimientoRepository()


@bp.route('/movimientos')
@authorize()
def index():
    if not request.is_xhr:
        return render_template('movimientos/index.html')

    search = request.args.get('queries[search]', '')
    limit = request.args.get('perPage', 0)
    offset = request.args.get('offset', 0)

    movimientos = mov_repo.get_list(search, limit, offset)

    def format_mov(mov):
        return {
            'id': mov.id,
            'encuestador': mov.encuestador,
            'fecha': mov.fecha.strftime('%Y-%m-%d'),
            'institucion': mov.institucion,
            'codigo': mov.codigo,
            'usuario': mov.usuario.name
        }

    return jsonify({
        'registros': [format_mov(m) for m in movimientos[1]],
        'total': movimientos[0]
    })


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

        mov_repo.persist(mov)

        observer = CreateObserver()
        mov.suscribe(observer)
        mov.notify(session['user_login'])

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
        form.populate_obj(mov)

        mov_repo.persist(mov)

        return redirect(url_for('.index'))

    return render_template('/movimientos/form.html',
                           form=form,
                           espaciamientos=ESPACIAMIENTOS)


@bp.route('/movimientos/delete/<int:id>', methods=['POST'])
@authorize(UserRole.user)
def delete(id):
    mov = mov_repo.get_by_id(id)

    mov_repo.delete(mov)

    observer = DeleteObserver()
    mov.suscribe(observer)
    mov.notify(session['user_login'])

    return redirect(url_for('.index'))


@bp.route('/movimientos/view/<int:id>')
@authorize()
def view(id):
    movimiento = mov_repo.get_by_id(id)

    return render_template('/movimientos/view.html',
                           mov=movimiento,
                           enums=masas.enums)


@bp.route('/movimientos/download/<int:id>')
@authorize()
def download(id):
    movimiento = mov_repo.get_by_id(id)

    output_html = render_template('/movimientos/view.html',
                                  mov=movimiento,
                                  enums=masas.enums)

    styles = ['./masas/static/css/print.css']

    pdf = HTML(string=output_html).write_pdf(stylesheets=styles)

    response = current_app.response_class(pdf, mimetype='application/pdf')

    response.headers.add('Content-Disposition',
                         'attachment',
                         filename='movimiento-' + movimiento.codigo + '.pdf')

    return response
