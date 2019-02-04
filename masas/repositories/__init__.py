from masas.core.database import db_session


class BaseRepository:
    def persist(self, obj):
        if not obj.id:
            db_session.add(obj)

        db_session.commit()

    def delete(self, obj):
        db_session.delete(obj)
        db_session.commit()
