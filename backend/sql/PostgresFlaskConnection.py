from app import db
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime


class PostgresFlaskConnectionClass:
    def __init__(self):
        # Establish connection string variables
        self.host = 'sequoiapostgres1.postgres.database.azure.com'
        self.port = 5432
        self.database = 'seq_app'
        self.username = 'sequoiauser'
        self.password = 'Sequoia_2023'

        self.connectionString = None

    def getConnectionString(self):
        self.connectionString = f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
        return self.connectionString

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


# if __name__ == '__main__':
#     testFlaskConnection = PostgresFlaskConnectionClass()
#     connectionString = testFlaskConnection.getConnectionString()
#     print(connectionString)
