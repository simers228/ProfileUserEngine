import sqlalchemy
from sqlalchemy import create_engine, inspect, text, insert, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostgresConnection:
    def __init__(self, sslmode='Require'):
        self.host = 'sequoiapostgres1.postgres.database.azure.com'
        self.port = 5432
        self.database = 'seq_app'
        self.username = 'sequoiauser'
        self.password = 'Sequoia_2023'
        self.sslmode = sslmode
        self.ssl_root_cert = './DigiCertGlobalRootCA.crt.pem'

        self.engine = None
        self.session = None
        self.metadata = None

    def __str__(self):
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

    def testTable(self):
        currentDatabaseQuery = text("SELECT * from tbl_LinkedinExperience")
        result = self.session.execute(currentDatabaseQuery)
        for i in result:
            print(i)

    def selectStatement(self, statement='SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != \'pg_catalog\' AND schemaname != \'information_schema\';'):
        # returns a list of the entries in the table - should return a dataframe at some point
        # Check statement for obvious syntax errors that will cause the SQL to not run
        if (self.errorCheck(statement)):
            # If the error check is true

            selectQuery = text(statement)
            selectResult = self.session.execute(selectQuery)
            selectReturn = []
            # depricate when this class is implemeneted and tested further
            if statement == 'SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != \'pg_catalog\' AND schemaname != \'information_schema\';':
                # if default statement
                for db in selectResult:
                    selectReturn.append(db)  # append to a list
                # return list of tables available
                return 'Choose a table to select from: ' + str(selectReturn)
            else:
                # custom select statement
                for i in selectResult:
                    selectReturn.append(i)  # append to a list
                return str(selectReturn)

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

    def main(self):
        '''
        # Define the variables in the connection string
        hostname = 'sequoiapostgres1.postgres.database.azure.com' # Public IP for my house hold - consider making this a hidden variable
        port = 5432 # Default postgres port - should never change
        database = 'seq_app' # Main DB for production - will be dev instance at some point
        username = 'sequoiauser' # User with CRUD privileges
        password = 'Sequoia_2023' # Make hidden variable asap
        '''

        insertRecruiterOptions.connect()
        # print(insertRecruiterOptions)
        # result = insertRecruiterOptions.selectStatement('SELECT * from tbl_linkedinexperience;')
        updateTable = 'tbl_recruiteroptions'

        valueList = ['userTest4', 'positionTest',
                     'locationTest', 'jobLocationTest', 'domainTest']

        result = insertRecruiterOptions.insertStatement(
            updateTable,  valueList)
        print(result)
        insertRecruiterOptions.disconnect()

        return 'Adding this functionality later'


# Sample code to call the SQL connection
insertRecruiterOptions = PostgresConnection()  # obfuscate password asap
insertRecruiterOptions.main()
