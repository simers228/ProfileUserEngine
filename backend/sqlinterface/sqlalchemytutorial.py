import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import MetaData
from database_setup import test


class SQLTutorial:
    def __init__(self):
        self.version = sqlalchemy.__version__

        self.host = 'sequoiapostgres1.postgres.database.azure.com'
        self.port = 5432
        self.database = 'seq_app'
        self.username = 'sequoiauser'
        self.password = 'Sequoia_2023'  # obfuscate password asap

        self.engine = None
        self.session = None

        # init meta data
        self.metadata_obj = MetaData()

        self.stmnt = None

    def __repr__(self):
        # Use to return values to the programmer
        # __str__ is optional for use to return human readable expressions
        return (
            f'SQL Alchemy version >> {self.version},\n'
            f'Host name           >> {self.host}\n'
            f'Database name       >> {self.database}\n'
            f'Engine              >> {self.engine}\n'
            f'Insert compile      >> {self.stmnt}\n'
        )

    def createEngine(self):
        # Uses a "lazy initialization"
        # This means creating the engine does not make a connection to the db
        connectionString = f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
        self.engine = create_engine(connectionString)

    def coreInsert(self):
        # Example function for to generate an insert statement using core
        # Will likely use ORM version over this
        self.stmnt = insert(table_name).values(username='aidan',
                                               password='Big23', created='2023-1-1')
        return self.stmnt


if ("__name__ = ", __name__):
    sqlobject = SQLTutorial()

    print(sqlobject)
