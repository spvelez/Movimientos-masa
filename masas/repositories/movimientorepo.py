from masas.models.movimiento import Movimiento
from masas.repositories import BaseRepository


class MovimientoRepository(BaseRepository):
    def get_all(self):
        return Movimiento.query.all()

    def get_by_id(self, id):
        return Movimiento.query.filter(Movimiento.id == id).first()
