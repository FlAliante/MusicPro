from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# https://docs.sqlalchemy.org/en/14/core/engines.html
# postgres://username:password@host:port/database
# mysql://username:password@host:port/database
uri = 'mysql://eja6vsq4rh1hw5pe:h341m14hjbajg524@migae5o25m2psr4q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ynghoqdpmk0i149y'
engine = create_engine(uri, poolclass=NullPool)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # import models.broker__c
    Base.metadata.create_all(bind=engine)