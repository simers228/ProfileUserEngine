from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime
from test_DatabaseSetup import *  # un-comment this for when testing
from sqlalchemy.orm import sessionmaker


class PostgresFlaskConnectionClass:
    def __init__(self):
        # Establish connection string variables
        self.host = 'sequoiapostgres1.postgres.database.azure.com'
        self.port = 5432
        self.database = 'seq_app'
        self.username = 'sequoiauser'
        self.password = 'Sequoia_2023'

        # Creating the connection
        self.connectionString = None
        self.engine = None
        self.session = None

    def __repr__(self):
        return ("connection string >> ", self.connectionString)

    def getConnectionString(self):
        self.connectionString = f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
        return self.connectionString

    def createSession(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return

    def createEngine(self):
        self.engine = create_engine(self.getConnectionString())
        return

    def setDatabase(self, database):
        self.database = database
        return

    def getDatabase(self):
        return self.database

    def getSession(self):
        return self.session

    def endConnection(self):
        """Disconnect from the PostgreSQL server."""
        self.session.close()
        self.engine.dispose()
        return

    def startConnection(self):
        '''Starts the connection by creating a session'''
        self.createEngine()
        self.createSession()
        return


if __name__ == '__main__':
    testFlaskConnection = PostgresFlaskConnectionClass()
    testFlaskConnection.startConnection()
    result = testFlaskConnection.getSession().query(tbl_linkedin).all()
    testFlaskConnection.endConnection()
    print(result)
