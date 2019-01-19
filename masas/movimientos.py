from flask import (
     Blueprint, flash, render_template, redirect, request, session, url_for
)

bp = Blueprint('movimientos', __name__, template_folder='templates')


@bp.route('/movimientos')
def index():
    return render_template('movimientos/index.html')


@bp.route('/movimientos/create')
def create():
    return render_template('movimientos/form.html')
