from sqlalchemy import create_engine, orm

from app import app

def create_session():
    """
    Creates a db session
    """
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(db_uri)
    sessionmaker = orm.sessionmaker(bind=engine)
    session = orm.scoped_session(sessionmaker)

    return session
