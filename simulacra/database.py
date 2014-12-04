from simulacra.config import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(config.get('database', 'DATABASE_URI', True), #convert_unicode=True) #, echo=True)
                       connect_args={'client_encoding': 'utf8'})
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
#    import simulacra.models
    Base.metadata.create_all(bind=engine)
