from sqlalchemy import or_

from masas.core.database import db_session
from masas.models.user import User
from masas.repositories import BaseRepository


class UserRepository(BaseRepository):
    def get_list(self, search, limit, offset):
        q = db_session.query(User)

        if search:
            q = q.filter(or_(User.login.ilike(search + '%'),
                             User.name.ilike('%' + search + '%')))

        rows = q.limit(limit).offset(offset).all()
        count = q.count()

        return (count, rows)

    def get_by_id(self, id):
        return User.query.filter(User.id == id).first()

    def get_by_login(self, login):
        return User.query.filter(User.login == login).first()
