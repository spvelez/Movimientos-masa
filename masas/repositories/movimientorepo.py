from sqlalchemy import or_

from masas.core.database import db_session
from masas.models.movimiento import Movimiento
from masas.repositories import BaseRepository


class MovimientoRepository(BaseRepository):
    def get_list(self, search, limit, offset):
        q = db_session.query(Movimiento)

        if search:
            q = q.filter(or_(Movimiento.encuestador.ilike('%' + search + '%'),
                             Movimiento.codigo.ilike(search + '%')))

        rows = q.limit(limit).offset(offset).all()
        count = q.count()

        return (count, rows)

    def get_by_id(self, id):
        return Movimiento.query.filter(Movimiento.id == id).first()
