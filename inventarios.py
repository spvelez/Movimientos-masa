from flask import (
     Blueprint, flash, render_template, redirect, request, session, url_for
)

bp = Blueprint('inventario', __name__, template_folder='templates')


@bp.route('/inventarios')
def index():
    return render_template('inventarios/index.html')


@bp.route('/inventarios/create')
def create():
    return render_template('inventarios/form.html')
