import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

# From: https://github.com/HOllarves/Udacity-SQL-Alchemy/blob/master/
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class test(Base):
    '''
    test table class
    '''

    __tablename__ = 'test'

    username = Column(String)
    password = Column(String)
    created = Column(DateTime)


engine = create_engine('connection string')


Base.metadata.create_all(engine)

# From a different part of this repo
engine = create_engine('connection string')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
insertStmnt = test(username="aidan", password=123,
                   created=datetime.datetime.now())

session.add(insertStmnt)
session.commit()
