from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime
# from test_DatabaseSetup import * # un-comment this for when testing
from DatabaseSetup import *
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

        # For holding query results
        self.recentSelectResult = None

    def __repr__(self):
        return ("select result >> ", self.recentSelectResult)

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

    def disconnect(self):
        """Disconnect from the PostgreSQL server."""
        self.session.close()
        self.engine.dispose()

    def setHost(self, host):
        self.host = host
        return

    def getHost(self):
        return self.host

    def setPort(self, port):
        self.port = port
        return

    def getPort(self):
        return self.port

    def setDatabase(self, database):
        self.database = database
        return

    def getDatabase(self):
        return self.database

    def select(self, tableName):
        '''
        Run this to perform a select query
        Currently only returns the first line in the query
        '''
        self.createEngine()
        self.createSession()
        result = self.session.query(tableName).first()
        self.disconnect()
        self.recentSelectResult = result
        return result


if __name__ == '__main__':
    testFlaskConnection = PostgresFlaskConnectionClass()
    result = testFlaskConnection.select(tbl_linkedin)
    print(result)
