import click
from flask import current_app
from flask.cli import with_appcontext

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(current_app.config['DB_CONNECTION'], echo=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))

DbModel = declarative_base()
DbModel.query = db_session.query_property()


@click.command('init-db')
@with_appcontext
def init_db_command():
    from masas.models import movimiento
    from masas.models import user

    DbModel.metadata.create_all(bind=engine)


def close_db(exception=None):
    db_session.remove()
