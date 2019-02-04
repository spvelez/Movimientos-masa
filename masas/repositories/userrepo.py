from masas.models.user import User
from masas.repositories import BaseRepository


class UserRepository(BaseRepository):
    def get_all(self):
        return User.query.all()

    def get_by_id(self, id):
        return User.query.filter(User.id == id).first()

    def get_by_login(self, login):
        return User.query.filter(User.login == login).first()
