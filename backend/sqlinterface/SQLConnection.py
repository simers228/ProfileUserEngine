import sqlalchemy
from sqlalchemy import create_engine, inspect, text
import psycopg2

# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class PostgresConnection:
    def __init__(self, host, port, database, username, password, sslmode='Require'):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.sslmode = sslmode
        self.ssl_root_cert = './DigiCertGlobalRootCA.crt.pem'
        
        self.engine = None
        self.session = None

    def __str__(self):
        return('Yes, this works')

    def connect(self):
        """Connect to the PostgreSQL server using SQLAlchemy and psycopg2."""
        connectionString = f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}' #?sslmode={self.sslmode}&sslrootcert={self.ssl_root_cert}'
        self.engine = create_engine(connectionString)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # print("very nice connection")
        return self.session

    def disconnect(self):
        """Disconnect from the PostgreSQL server."""
        self.session.close()
        self.engine.dispose()

    def executeQuery(self, query, queryType):
        # Use to run any query
        # Other methods are for string handling
        # Not implementing now, but could be helpful if you want to combine some execution steps
        # case queryType == 'insert':
        #     selectQuery = text(statement)
        #     selectResult = self.session.execute(selectQuery)
        return
            

        
    
    def testTable(self):
        currentDatabaseQuery = text("SELECT * from tbl_LinkedinExperience")
        result = self.session.execute(currentDatabaseQuery)
        for i in result:
            print(i)

    def selectStatement(self, statement='SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != \'pg_catalog\' AND schemaname != \'information_schema\';'):
        # returns a list of the entries in the table - should return a dataframe at some point
        if(self.errorCheck(statement)): # Check statement for obvious syntax errors that will cause the SQL to not run
            # If the error check is true

            selectQuery = text(statement)
            selectResult = self.session.execute(selectQuery)
            selectReturn = []
            if statement == 'SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != \'pg_catalog\' AND schemaname != \'information_schema\';': # depricate when this class is implemeneted and tested further
                # if default statement
                for db in selectResult:
                    selectReturn.append(db) # append to a list
                return 'Choose a table to select from: ' + str(selectReturn) # return list of tables available
            else:
                # custom select statement
                for i in selectResult:
                    selectReturn.append(i) # append to a list
                return str(selectReturn)
            
    def updateStatement(self, statement):
        # An update statement that allows for one update query
        # Can make this more dynamic
        # Maybe return the updated table in a select?
        if(self.errorCheck(statement)): # Check statement for obvious syntax errors that will cause the SQL to not run
            updateQuery = text(statement)
            updateResult = self.session.execute(updateQuery)

    def insertStatement(self, table, valueList, schema='public'):
        #Error checking
        self.table = table
        if type(valueList) != list:
            print("Values must be in a list")
            return

        tableColumns = self.generateColumns(schema, table)
        
        #Values Generate
        valueString = ''
        index = 0
        while index < len(tableColumns):
            if len(tableColumns) - 1 == index:
                valueString += f'\'{valueList[index]}\'' #{tableColumns[index]}=
                break
            else:
                valueString += f'\'{valueList[index]}\', ' #{tableColumns[index]}=
                index += 1

        # Heavy string manipulation here, some of it is likely redundant
        insertStatement = f"INSERT INTO {schema}.{table} ({', '.join(tableColumns)}) VALUES ({valueString});"
        
        # Other args takes for an insert vs. a select - look into documentation later
        insertQuery = text(insertStatement)
        insertResult = self.session.execute(insertQuery)
   

        #print('Your table is updated')
        return insertResult


    def errorCheck(self, statement):
         if statement[-1] == ';':
             return True
         else:
             print('Error: SQL statement does not end with ";"')
             return False
         
    def generateColumns(self, schema, table):
        # Returns the columns of a given table in a list
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table)
        column_names = [column['name'] for column in columns]
        return column_names




    def main(self):

        # Establish the variables in the class
        #conn = PostgresConnection(hostname, port, database, username, password)
        self.connect()
        self.disconnect()

        #print() # Show how variables are called in class, can also be set

        # List current databases
        #self.listCurrentDatabase()

        #self.disconnect() # call the disconnect function to end the connection

        return 'Adding this functionality later'

'''
# Define the variables in the connection string
hostname = 'sequoiapostgres1.postgres.database.azure.com' # Public IP for my house hold - consider making this a hidden variable
#hostname = '20.169.176.238'
port = 5432 # Default postgres port - should never change
database = 'seq_app' # Main DB for production - will be dev instance at some point
username = 'sequoiauser' # User with CRUD privileges
password = 'Sequoia_2023' # Make hidden variable asap
'''
# Sample code to call the SQL connection
insertRecruiterOptions = PostgresConnection('sequoiapostgres1.postgres.database.azure.com', 5432,'seq_app','sequoiauser','Sequoia_2023') # obfuscate password asap
insertRecruiterOptions.connect()
#print(insertRecruiterOptions)
#result = insertRecruiterOptions.selectStatement('SELECT * from tbl_linkedinexperience;')
result = insertRecruiterOptions.insertStatement('tbl_recruiteroptions', ['userTest','positionTest','locationTest','jobLocationTest','domainTest'])
print(result)
insertRecruiterOptions.disconnect()


