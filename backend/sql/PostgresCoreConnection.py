import sqlalchemy
from sqlalchemy import create_engine, inspect, text, insert, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime


class PostgresCoreConnectionClass:
    def __init__(self, sslmode='Require'):
        # Establish connection string
        self.host = 'sequoiapostgres1.postgres.database.azure.com'
        self.port = 5432
        self.database = 'seq_app'
        self.username = 'sequoiauser'
        self.password = 'Sequoia_2023'  # obfuscate password asap
        self.sslmode = sslmode
        self.ssl_root_cert = './DigiCertGlobalRootCA.crt.pem'

        # Manage session
        self.engine = None
        self.session = None
        self.metadata = None

    def __repr__(self):
        print(f'host > {self.host}')
        print(f'database > {self.database}')
        return ('Yes, this works')

    def connect(self):
        """Connect to the PostgreSQL server using SQLAlchemy and psycopg2."""
        connectionString = f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'  # ?sslmode={self.sslmode}&sslrootcert={self.ssl_root_cert}'
        self.engine = create_engine(connectionString)

        # Bind the engine to the metadata
        self.metadata = MetaData()

        # Reflect the existing database tables
        self.metadata.reflect(bind=self.engine)

        # Make the session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        return self.session

    def disconnect(self):
        """Disconnect from the PostgreSQL server."""
        self.session.close()
        self.engine.dispose()

    def selectStatement(self, statement='SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != \'pg_catalog\' AND schemaname != \'information_schema\';'):
        # returns a list of the entries in the table - should return a dataframe at some point
        # Check statement for obvious syntax errors that will cause the SQL to not run
        if (self.errorCheck(statement)):
            # If the error check is true
            self.connect()
            selectQuery = text(statement)
            selectResult = self.session.execute(selectQuery)
            selectReturn = []
            # depricate when this class is implemeneted and tested further
            if statement == 'SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != \'pg_catalog\' AND schemaname != \'information_schema\';':
                # if default statement
                for db in selectResult:
                    selectReturn.append(db[0].strip())
                # return list of tables available
                self.disconnect()
                return 'Choose a table to select from: ' + selectReturn
            else:
                # custom select statement
                for line in selectResult:
                    cleaned_line = [col.strip() if isinstance(
                        col, str) else col for col in line]
                    selectReturn.append(cleaned_line)
                self.disconnect()
                return selectReturn

    def updateStatement(self, statement):
        # An update statement that allows for one update query
        # Can make this more dynamic
        # Maybe return the updated table in a select?
        # Check statement for obvious syntax errors that will cause the SQL to not run
        if (self.errorCheck(statement)):
            updateQuery = text(statement)
            updateResult = self.session.execute(updateQuery)

    def insertStatement(self, tableName, valueList, schema='public'):
        # Error checking
        if type(valueList) != list:
            print("Values must be in a list")
            return

        table = Table(tableName, self.metadata, autoload=True)
        insertStatement = table.insert().values(
            dict(zip(table.columns.keys(), valueList)))

        with self.engine.begin() as connection:
            connection.execute(insertStatement)

        return insertStatement  # insertResult

    def errorCheck(self, statement):
        # Ensure SQL statements ends in a ";"
        if statement[-1] == ';':
            return True
        else:
            print('Error: SQL statement does not end with ";"')
            return False

    def generateColumns(self, schema, table):
        # Returns the columns of a given table in a list
        # Helper function that is not currently being called
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table)
        column_names = [column['name'] for column in columns]
        return column_names

    def getEngine(self):
        return self.engine

    def main(self):
        '''
        # Define the variables in the connection string
        hostname = 'sequoiapostgres1.postgres.database.azure.com' # Public IP for my house hold - consider making this a hidden variable
        port = 5432 # Default postgres port - should never change
        database = 'seq_app' # Main DB for production - will be dev instance at some point
        username = 'sequoiauser' # User with CRUD privileges
        password = 'Sequoia_2023' # Make hidden variable asap
        '''

        self.connect()

        username = 'aidang1'

        result = self.selectStatement(
            f'SELECT * FROM tbl_users WHERE username = \'{username}\';')

        self.disconnect

        return result


# Sample code to call the SQL connection
# conn = PostgresConnection()
# print(conn.main())
