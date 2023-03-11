from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#      https://docs.sqlalchemy.org/en/14/core/engines.html
#      postgres://username:password@host:port/database
#      mysql://eja6vsq4rh1hw5pe:h341m14hjbajg524@migae5o25m2psr4q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ynghoqdpmk0i149y
#uri = 'postgres://ofejsmvvyzksab:0655aede6a5679c52cde16e570ff0bcd7cf31963c5cdf78bdb2a2eb4358af4e1@ec2-44-206-197-71.compute-1.amazonaws.com:5432/d7dhj0k7r6c8cr'
uri = 'mysql://eja6vsq4rh1hw5pe:h341m14hjbajg524@migae5o25m2psr4q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ynghoqdpmk0i149y'
engine = create_engine(uri, poolclass=NullPool)
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # import models.broker__c
    Base.metadata.create_all(bind=engine)