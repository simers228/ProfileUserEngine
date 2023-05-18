import sqlalchemy


class SQLTutorial:
    def __init__(self):
        self.version = sqlalchemy.__version__

        self.host = 'sequoiapostgres1.postgres.database.azure.com'
        self.port = 5432
        self.database = 'seq_app'
        self.username = 'sequoiauser'
        self.password = 'Sequoia_2023'  # obfuscate password asap

    def __repr__(self):
        # Use to return values to the programmer
        # __str__ is optional for use to return human readable expressions
        return (
            f'SQL Alchemy version >> {self.version},\n'
            f'host name           >> {self.host}\n'
            f'database name       >> {self.database}\n'
        )


if ("__name__ = ", __name__):
    sqlobject = SQLTutorial()
    print(sqlobject)
